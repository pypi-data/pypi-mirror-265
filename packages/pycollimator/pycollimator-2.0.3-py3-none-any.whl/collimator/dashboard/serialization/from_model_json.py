# Copyright (C) 2024 Collimator, Inc.
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, version 3. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General
# Public License for more details.  You should have received a copy of the GNU
# Affero General Public License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

from __future__ import annotations

import json
import traceback
from uuid import uuid4

from collimator.framework import (
    Diagram,
    DiagramBuilder,
    Parameter,
    SystemBase,
    SystemCallback,
    LeafSystem,
)
from collimator.library import ReferenceSubdiagram
from collimator.simulation import (
    ResultsMode,
    ResultsOptions,
    SimulatorOptions,
)
from collimator.experimental.acausal import Network, Compiler

from . import block_interface, model_json

import dataclasses
import math
from typing import Any

import jax.numpy as jnp
import numpy as np

from collimator import logging
from collimator.framework.error import (
    BlockInitializationError,
    BlockParameterError,
    CollimatorError,
    LegacyBlockConfigurationError,
    ModelInitializationError,
    StaticError,
)
from collimator.lazy_loader import LazyLoader

control = LazyLoader("control", globals(), "control")


"""
Layer between the Collimator app JSON output and the sim engine.
Presently, this works for model.json+list[submodel-uuid-ver.json] content
from both simworkerpy(wildcat) and simworker(go)(cmlc).

Processing steps:
1] The classes in types.py are used to "read" the json, packaging convinently
Not ideal, but there is some transformation that happen here.
Specifically, model.json.parameters dict is transformed to match List[ParameterDefinition]
so that the top level diagram and all submodel diagrams can be treated identically
w.r.t. parameter namespace handling at later loading stages.

2] visit all the model subdiagrams by depth first search through the json.
create node name_path ids, and a dict diagrams[subdiagram_node_id]=LoadCtxtDiagram (e.g. most the raw json content).

3] visit all the elements of diagrams dict, and build a wildcat diagram object for each, composing them as we go.

"""


@dataclasses.dataclass
class SimulationContext:
    model_uuid: str
    diagram: Diagram
    results_options: ResultsOptions
    recorded_signals: dict[str, SystemCallback]
    simulator_options: SimulatorOptions = None


@dataclasses.dataclass
class AcausalDiagram:
    blocks: dict[str, dict]
    acausal_links: dict[str, model_json.Link]
    causal_inlinks: dict[str, model_json.Link]
    causal_outlinks: dict[str, model_json.Link]


def loads_model(
    model_json_str: str,
    namespace: dict[str, Any] = None,
) -> SimulationContext:
    """Load a model from a JSON string.

    Reference submodels must be registered before calling this function.
    """
    model_dict = json.loads(model_json_str)
    return load_model(model_dict, namespace)


def load_model(
    model_json_obj: dict,
    namespace: dict[str, Any] = None,
) -> SimulationContext:
    """Load a model from a parsed JSON object.

    Reference submodels must be registered before calling this function.
    """
    if namespace is None:
        namespace = {}

    model = model_json.Model.from_dict(model_json_obj)


    model_parameters = {}
    for param_name, param in model.parameters.items():
        if param.is_string:
            model_parameters[param_name] = param.value
        else:
            value = eval_parameter(param.value, namespace, namespace)
            model_parameters[param_name] = Parameter(name=param_name, value=value)

    root_namespace = namespace
    root_namespace.update(model_parameters)

    root_id = "root"

    # traverse the entire model, and extract the blocks/links/etc.
    # of each acausal diagram.
    # NOTE: when isolating AcausalDiagrams, we need to identify then
    # with name_path that starts with 'root' because otherwise the
    # name_path for a AcausalDiagram at the root level would have empty
    # string as id.
    acausal_diagrams = identify_acausal_networks(
        name=root_id,
        diagram=model.diagram,
        subdiagrams=model.subdiagrams,
        parent_ui_id_path=[root_id],
        parent_path=[root_id],
        ui_id=root_id,
    )

    recorded_signals = {}
    diagram = make_subdiagram(
        root_id,
        model.diagram,
        model.subdiagrams,
        model.state_machines,
        acausal_diagrams,
        parent_path=[],
        parent_ui_id_path=[],
        ui_id=model.diagram.uuid,
        namespace_params=root_namespace,
        global_discrete_interval=model.configuration.sample_time,
        record_mode=model.configuration.record_mode,
        recorded_signals=recorded_signals,
        start_time=model.configuration.start_time,
        model_parameters=model_parameters,
    )

    results_options = None
    if model.configuration:
        results_options, simulator_options = simulation_settings(
            model.configuration, recorded_signals=recorded_signals
        )

    return SimulationContext(
        model_uuid=model.uuid,
        diagram=diagram,
        results_options=results_options,
        recorded_signals=recorded_signals,
        simulator_options=simulator_options,
    )


def eval_parameter(value: str, _globals: dict, _locals: dict):
    # Block parameters can be left empty, but JSON may contain null or "None"
    if not value or value == "None":
        return None
    p = eval(str(value), _globals, _locals)
    # Rules for user-input parameters:
    # - if explicitly given as an array with dtype, use that dtype
    # - if boolean, use as given
    # - otherwise, convert to a numpy array
    if not hasattr(p, "dtype") and not isinstance(p, bool):
        p = np.array(p)
        # if the array has integer dtype convert to float. Note that
        # this case will still not be reached if the parameter is explicitly
        # declared as an array with integer datatype.  However, this will
        # promote inputs like `"0"` or `"[1, 0]"` to floats.
        if issubclass(p.dtype.type, np.integer):
            p = p.astype(float)
    return p


def eval_parameters(
    default_parameters: list[model_json.ParameterDefinition] = None,
    instance_parameters: dict[str, model_json.Parameter] = None,
    call_site_namespace: dict[str, Any] = None,
    name_path: list[str] = None,
    ui_id_path: list[str] = None,
):
    # parameter handling.
    # at this point we have the following:
    # 1] diagrams[block_id].default_parameters
    #   these are from the submodel-uuid-ver.json[parameter_definitions].
    #   these are the definitions and defaults for all parameters in the name space of the submodel
    # 2] instance_parameters
    #   these are the parameter values from the instance of the submodel. this must be a subset of 1]
    #   this dict is typically limited to those params which have been modified from their default value.
    #   the values of these should have been evaluated in the context of the parent of the instance.
    # 3] call_site_namespace
    #   these are the parameters in the name space of the parent.
    #   these are only used here because before getting here, only the instance parameters
    #   have been evaluated in the parent name space. if a parameters has not been modified,
    #   then we use the default value from 1] but we need to evaluate it in the parent name space.
    #
    # Note: reference submodels have a 'protected' parameter names space. parents can only pass
    # parameter values through the submodels defined parameters. i.e. there is no shared name space
    # between the reference submodel instance and its parent.

    if default_parameters is None:
        default_parameters = []
    if call_site_namespace is None:
        call_site_namespace = {}
    if instance_parameters is None:
        instance_parameters = {}

    # We don't technically need to pass np and jnp here, but it makes them explicitly
    # available in the local `eval` environment.
    _locals = {
        **call_site_namespace,
        "np": np,
        "jnp": jnp,
        "math": math,
        "false": False,
        "true": True,
    }

    def _eval(param_name, value: str):
        try:
            return eval_parameter(value, globals(), _locals)
        # We will probably want to be much more discriminating with respect to what gets
        # caught here. This uses exception chaining to record the offending block id
        # and parameter name.
        except Exception as exc:
            traceback.print_exc()
            raise BlockParameterError(
                name_path=name_path, ui_id_path=ui_id_path, parameter_name=param_name
            ) from exc

    # multi round eval is required in case we have parameters that reference other parameters.
    # FIXME: WC-112 this should not be allowed
    def _multi_round_eval(params, eval_fn):
        eval_results = {}
        max_eval_depth = 10
        for i in range(max_eval_depth):
            need_eval = False
            for pname, p in params.items():
                try:
                    eval_results[pname] = eval_fn(pname, p)
                except BlockParameterError as exc:
                    if i == max_eval_depth - 1:
                        raise exc
                    need_eval = True
            _locals.update(eval_results)
            if not need_eval:
                break
        return eval_results

    def _eval_param_def(pname, p):
        if p.default_value != "":
            return _eval(pname, p.default_value)
        return None

    def _eval_param(pname, p):
        if p.is_string:
            return p.value
        return _eval(pname, p.value)

    default_values = _multi_round_eval(
        {p.name: p for p in default_parameters},
        _eval_param_def,
    )
    instance_values = _multi_round_eval(
        instance_parameters,
        _eval_param,
    )

    default_values.update(instance_values)
    return default_values


def eval_init_script(
    init_script_file_name: str,
    namespace_params: dict = None,
    name_path: list[str] = None,
    ui_id_path: list[str] = None,
) -> dict:
    # FIXME: don't do this:
    # We don't technically need to pass np and jnp here, but it makes them explicitly
    # available in the local `exec` environment. a user could also do these imports.
    # "__main__": {} is necessary for script of the form
    #   imports ...
    #   a = 1
    #   def f(b):
    #       return a+b
    #   out_0 = f(2)
    # withotu getting "a not defined" error.

    namespace_params = namespace_params or {}

    _locals = {
        **namespace_params,
        "np": np,
        "jnp": jnp,
        "control": control,
        "__main__": {},
    }

    with open(init_script_file_name, "r") as file:
        _init_script_code = file.read()

    try:
        exec(_init_script_code, _locals, _locals)
    except Exception as e:
        raise ModelInitializationError(
            f"Failed to execute init_script {init_script_file_name}",
            name_path=name_path,
            ui_id_path=ui_id_path,
        ) from e

    # _locals will be pretty messy after exec() since it wil contain all the stuff
    # python puts in globals for any execution. doesn't matter, this globals env
    # is only retained for parameter evaluation.
    return _locals


def GroupBlock(
    block_spec: model_json.Node,
    global_discrete_interval: float,
    subdiagrams: dict[str, model_json.Diagram],
    state_machines: dict[str, model_json.LoadStateMachine],
    acausal_diagrams: dict[str, AcausalDiagram],
    parent_path: list[str],
    parent_ui_id_path: list[str],
    record_mode: str = "selected",
    namespace_params: dict[str, Any] = None,
    block_overrides=None,
    recorded_signals=None,
    start_time: float = 0.0,
) -> Diagram:
    return make_subdiagram(
        block_spec.name,
        subdiagrams.get_diagram(block_spec.uuid),
        subdiagrams,
        state_machines,
        acausal_diagrams,
        ui_id=block_spec.uuid,
        parent_path=parent_path,
        parent_ui_id_path=parent_ui_id_path,
        global_discrete_interval=global_discrete_interval,
        namespace_params=namespace_params or {},
        block_overrides=block_overrides,
        record_mode=record_mode,
        recorded_signals=recorded_signals,
        start_time=start_time,
    )


def register_reference_submodel(ref_id: str, model: model_json.Model):
    def _make_subdiagram_instance(
        instance_name: str,
        parameters,
        uuid: str = None,
        parent_path: list[str] = None,
        parent_ui_id_path: list[str] = None,
        record_mode: str = "selected",
        recorded_signals: dict[str, SystemCallback] = None,
        global_discrete_interval: float = 0.1,
        start_time: float = 0.0,
    ):
        if uuid is None:
            uuid = str(uuid4())
        diagram = dataclasses.replace(model.diagram, uuid=uuid)
        return make_subdiagram(
            instance_name,
            diagram,
            model.subdiagrams,
            model.state_machines,
            acausal_diagrams=None,  # FIXME: ignoring acausal diagram under submodels
            namespace_params=parameters,
            ui_id=uuid,
            parent_path=parent_path,
            parent_ui_id_path=parent_ui_id_path,
            global_discrete_interval=global_discrete_interval,
            record_mode=record_mode,
            recorded_signals=recorded_signals,
            start_time=start_time,
        )

    parameter_definitions = None
    if model.parameter_definitions:
        parameter_definitions = model.parameter_definitions
    elif model.parameters:
        # NOTE: simworker-go instantiates the submodel with parameters (dict of parameters)
        # see test_0080a.py for example.
        # So here we convert to parameter definitions (list of ParameterDefinition).
        logging.debug("Converting instantiated parameters to parameter definitions.")
        parameter_definitions = [
            model_json.ParameterDefinition(name=k, default_value=v.value)
            for k, v in model.parameters.items()
        ]

    parameters = eval_parameters(default_parameters=parameter_definitions)
    parameters = [Parameter(name=name, value=value) for name, value in parameters.items()]

    ReferenceSubdiagram.register(
        _make_subdiagram_instance,
        parameter_definitions=parameters,
        ref_id=ref_id,
    )


# FIXME: simplify this function. it's too long.
# pylint: disable=too-complex
# flake8: noqa: C901
def make_subdiagram(
    name: str,
    diagram: model_json.Diagram,
    subdiagrams: dict[str, model_json.Diagram],
    state_machines: dict[str, model_json.LoadStateMachine],
    acausal_diagrams: dict[str, AcausalDiagram],
    parent_ui_id_path: list[str] = None,
    parent_path: list[str] = None,
    ui_id: str = None,
    namespace_params=None,
    block_overrides: dict[str, SystemBase] = None,
    record_mode: str = "selected",
    recorded_signals: dict[str, SystemCallback] = None,
    global_discrete_interval: float = 0.1,
    start_time: float = 0.0,
    model_parameters: dict[str, model_json.Parameter] = None,
) -> Diagram:
    if namespace_params is None:
        namespace_params = {}

    if parent_path is None:
        parent_path = []

    if parent_ui_id_path is None:
        parent_ui_id_path = []

    # The "node_spec" passed here is the "node" specification that doesn't
    # contain the actual blocks. the info about the block tat constains the
    # subdiagram, e.g. submodel instance.

    # TODO: correctly handle RefSubmodelConfiguration features
    # (atomic, discrete_step)

    builder = DiagramBuilder()

    # I/O ports are considered "blocks" in the UI, so they need to be tracked
    # specificially (lists of block names)
    exported_inputs: list[str] = []
    exported_outputs: list[str] = []

    # needed for dereferencing node ids in link specs. this map is local to a
    # canvas.
    block_uuid_to_name: dict[str, str] = {}

    # block name to created object
    blocks: dict[str, SystemBase | Diagram] = {}

    # check if this canvas has an acausal diagram.
    if acausal_diagrams is not None:
        # NOTE: when isolating AcausalDiagrams, we need to identify then
        # with name_path that starts with 'root' because otherwise the
        # name_path for a AcausalDiagram at the root level would have empty
        # string as id.
        acausal_diagram_key = ".".join(["root"] + parent_ui_id_path)
        acausal_diagram = acausal_diagrams.get(acausal_diagram_key, None)
    else:
        acausal_diagram = None
    # if this canavas has an acausal diagram, produce the equivalent phleaf
    if acausal_diagram is not None:
        phleaf, inlinks_map, outlinks_map = build_acausal_network(
            acausal_diagram,
            namespace_params,
            name=".".join(["root"] + parent_path + ["phleaf"]),
            parent_path=parent_path,
            parent_ui_id_path=parent_ui_id_path,
        )
        blocks[phleaf.name] = phleaf
        builder.add(phleaf)
        acausal_links = acausal_diagram.acausal_links
        causal_inlinks = acausal_diagram.causal_inlinks
        causal_outlinks = acausal_diagram.causal_outlinks
    else:
        acausal_links = {}
        causal_inlinks = {}
        causal_outlinks = {}
        inlinks_map = {}
        outlinks_map = {}

    # process causal blocks
    for block_spec in diagram.nodes:
        block: SystemBase | Diagram = None

        # block names are used as locally (in this canvas) unique identifiers
        block_name = block_spec.name
        block_ui_id = block_spec.uuid
        block_uuid_to_name[block_ui_id] = block_name

        # these are used for rich errors before the block is created
        block_name_path = parent_path + [block_name]
        block_ui_id_path = parent_ui_id_path + [block_ui_id]

        if block_spec.type == "core.Inport":
            exported_inputs.append(block_name)
        elif block_spec.type == "core.Outport":
            exported_outputs.append(block_name)

        is_phealf_block = False

        try:
            # FIXME: refactor below contents of try into a function

            if block_overrides and block_name in block_overrides:
                # FIXME this was probably broken inside subdiagrams and looks extremely hacky anyway
                block_name_path_str = ".".join(block_name_path)
                block = block_overrides[block_name_path_str]

            # branches for recursing into subdiagrams
            elif block_spec.type == "core.ReferenceSubmodel":
                logging.debug(
                    "Creating reference submodel %s (ref id: %s) "
                    "with instance_parameters: %s, call_site_namespace: %s",
                    block_name,
                    block_spec.submodel_reference_uuid,
                    block_spec.parameters,
                    namespace_params,
                )

                # Note: only expressions are supported here, no string literals

                parameters = eval_parameters(
                    instance_parameters=block_spec.parameters,
                    call_site_namespace=namespace_params,
                    name_path=block_name_path,
                    ui_id_path=block_ui_id_path,
                )

                block = ReferenceSubdiagram.create_diagram(
                    block_spec.submodel_reference_uuid,
                    instance_parameters=parameters,
                    global_discrete_interval=global_discrete_interval,
                    record_mode=record_mode,
                    instance_name=block_name,
                    recorded_signals=recorded_signals,
                    parent_path=parent_path + [block_name],
                    parent_ui_id_path=parent_ui_id_path + [block_ui_id],
                    uuid=block_spec.uuid,
                    start_time=start_time,
                )
            elif block_spec.type in ("core.Group", "core.Submodel"):
                block = GroupBlock(
                    block_spec,
                    global_discrete_interval,
                    subdiagrams,
                    state_machines,
                    acausal_diagrams,
                    parent_path=parent_path + [block_name],
                    parent_ui_id_path=parent_ui_id_path + [block_ui_id],
                    namespace_params=namespace_params,
                    record_mode=record_mode,
                    recorded_signals=recorded_signals,
                    start_time=start_time,
                )
            # branch for normal 'blocks'. not subdiagrams.
            else:
                common_kwargs = {
                    "name": block_name,
                    "ui_id": block_ui_id,
                }
                parameters = eval_parameters(
                    instance_parameters=block_spec.parameters,
                    call_site_namespace=namespace_params,
                    name_path=block_name_path,
                    ui_id_path=block_ui_id_path,
                )
                # branches for 'special' blocks
                if block_spec.type == "core.StateMachine":
                    block = block_interface.get_block_fcn(block_spec.type)(
                        block_spec=block_spec,
                        discrete_interval=global_discrete_interval,
                        state_machine_diagram=state_machines[
                            block_spec.state_machine_diagram_id
                        ],
                        **common_kwargs,
                        **parameters,
                    )
                elif block_spec.type == "core.ModelicaFMU":
                    block = block_interface.get_block_fcn(block_spec.type)(
                        block_spec=block_spec,
                        discrete_interval=global_discrete_interval,
                        start_time=start_time,
                        **common_kwargs,
                        **parameters,
                    )
                elif block_spec.type[0:5] == "phys.":
                    # FIXME: the above condition is terrible
                    # NOTE: acausal blocks were already isolated and processed, nothing to do here.
                    # NOTE: we need to flag that the 'block' being processed is not a 'LeafSystem'
                    # to avoid further processing (only applicable to LeafSystems) being applied to it.
                    is_phealf_block = True
                else:
                    block = block_interface.get_block_fcn(block_spec.type)(
                        block_spec=block_spec,
                        discrete_interval=global_discrete_interval,
                        **common_kwargs,
                        **parameters,
                    )

                if block_spec.inputs and not is_phealf_block:
                    input_port_names = [port.name for port in block_spec.inputs]
                    for port_name, port in zip(input_port_names, block.input_ports):
                        port.name = port_name

                if block_spec.outputs and not is_phealf_block:
                    output_port_names = [port.name for port in block_spec.outputs]
                    for port_name, port in zip(output_port_names, block.output_ports):
                        port.name = port_name

            # NOTE: Here we assume that the port order is the same in the frontend and wildcat
            # Log anything with record=True
            if block_spec.outputs and recorded_signals is not None:
                for i, port in enumerate(block_spec.outputs):
                    if port.record or record_mode == "all":
                        if is_phealf_block:
                            if block_ui_id in outlinks_map.keys():
                                if i in outlinks_map[block_ui_id].keys():
                                    # when the block is part of a phleaf, we map its 'recorded'
                                    # ports to the corresponding phleaf port.
                                    port_id = outlinks_map[block_ui_id][i]
                                    port_path = parent_path + [block_name, port.name]
                                    port_path = ".".join(port_path)
                                    logging.debug("Recording %s", port_path)
                                    recorded_signals[port_path] = phleaf.output_ports[
                                        port_id
                                    ]
                            else:
                                # this port is an acausal port, do nothing.
                                continue
                        else:
                            port_path = parent_path + [block_name, port.name]
                            port_path = ".".join(port_path)
                            logging.debug("Recording %s", port_path)

                            if i < 0 or i >= len(block.output_ports):
                                # This unlikely error can happen when for instance there's
                                # an invalid JSON with more i/o ports than what wildcat
                                # defines (eg. old StateSpace blocks)
                                raise LegacyBlockConfigurationError(
                                    message=f"Output port index {i} out of range"
                                    f"({len(block.output_ports)}) for block {block.name}",
                                    name_path=block_name_path,
                                    ui_id_path=block_ui_id_path,
                                    port_index=i,
                                    port_name=port.name,
                                    port_direction="out",
                                )

                            recorded_signals[port_path] = block.output_ports[i]

            if not is_phealf_block:
                builder.add(block)
                blocks[block_name] = block

        except (StaticError, BlockInitializationError) as exc:
            raise exc
        except Exception as exc:
            traceback.print_exc()
            if isinstance(exc, CollimatorError):
                # Avoid repetition in the error message by only keeping this info in
                # the top-level error
                exc.name_path = None
                exc.system_id = None
            path = ".".join(block_name_path)
            raise BlockInitializationError(
                message=f"Failed to create block {path} of type {block_spec.type}",
                system=block,
                name_path=block_name_path,
                ui_id_path=block_ui_id_path,
            ) from exc

    # Export the input port of any Inport
    for input_port_id_key in exported_inputs:
        builder.export_input(blocks[input_port_id_key].input_ports[0])

    # Export the output port of any Outport
    for output_port_id_key in exported_outputs:
        builder.export_output(blocks[output_port_id_key].output_ports[0])

    for link in diagram.links:
        if (
            (link.src is None)
            or (link.dst is None)
            or (link.src.node not in block_uuid_to_name)
            or (link.dst.node not in block_uuid_to_name)
            or link.uuid in acausal_links.keys()  # handled in build_acausal_network()
        ):
            continue

        src_block_name = block_uuid_to_name[link.src.node]
        dst_block_name = block_uuid_to_name[link.dst.node]
        src_port_index = int(link.src.port)
        dst_port_index = int(link.dst.port)

        if acausal_diagram is not None:

            if link.uuid in causal_inlinks.keys():
                dst_block_name = phleaf.name
                dst_port_index = inlinks_map[link.dst.node][dst_port_index]
            elif link.uuid in causal_outlinks.keys():
                src_block_name = phleaf.name
                src_port_index = outlinks_map[link.src.node][src_port_index]
        else:
            # These unlikely errors can happen when for instance there's
            # an invalid JSON with more i/o ports than what wildcat
            # defines (eg. old StateSpace blocks)
            # NOTE: these errors cannot happen for phealf related links.
            if src_port_index < 0 or src_port_index >= len(
                blocks[src_block_name].output_ports
            ):
                raise LegacyBlockConfigurationError(
                    f"Invalid src port index {src_port_index} for block {blocks[src_block_name].name}",
                    name_path=block_name_path,
                    ui_id_path=block_ui_id_path,
                )
            elif dst_port_index < 0 or dst_port_index >= len(
                blocks[dst_block_name].input_ports
            ):
                raise LegacyBlockConfigurationError(
                    f"Invalid dst port index {dst_port_index} for block {blocks[dst_block_name].name}",
                    name_path=block_name_path,
                    ui_id_path=block_ui_id_path,
                )

        builder.connect(
            blocks[src_block_name].output_ports[src_port_index],
            blocks[dst_block_name].input_ports[dst_port_index],
        )

    return builder.build(name=name, ui_id=ui_id, parameters=model_parameters)


def identify_acausal_networks(
    name: str,
    diagram: model_json.Diagram,
    subdiagrams: dict[str, model_json.Diagram],
    parent_ui_id_path: list[str] = None,
    parent_path: list[str] = None,
    ui_id: str = None,
    acausal_diagrams: dict[str, AcausalDiagram] = None,
) -> dict[str, AcausalDiagram]:
    """
    Acausal diagrams are a subset of the diagram on a canvas. The subset is made up of
    all the acausal component blocks on the canvas, and all the link between two acausal
    ports of those blocks.
    Acausal diagrams cannot be processed the same way as causal diagrams, e.g. create one
    LeafSystem at a time, connect the inputs/outputs, and then 'build' the diagram. Acausal
    diagrams must have all components and network equations collection into one equation
    set, and from thei equation set a single LeafSystem (phleaf) is produce.
    Therefore, before the model traversal for creating LeafSystems and building diagrams,
    we have this model traversal which collects the acausal blocks and links that make
    up the acausal diagram in a given canvas. this data is retained, and then when the
    same canvas is reached in the second model traversal, first we will process the acausal
    block/inks to create the Acausal LeafSystem (phleaf), and integrate that into the
    rest of the diagram on that canvas replacing the acausal blocks and links that were
    there in the UI representation.
    In this traversal, there is no attempt to evaluate parameters, nor create class
    instances for blocks. The goal is only to isolate the subset of the diagram that is
    the acausal diagram. As such, we can treat submodels the same as groups.
    """

    if parent_path is None:
        parent_path = []

    if parent_ui_id_path is None:
        parent_ui_id_path = []

    # The "node_spec" passed here is the "node" specification that doesn't
    # contain the actual blocks. the info about the block that constains the
    # subdiagram, e.g. submodel instance.

    # acausal networks only supported within a single canvas for now
    if acausal_diagrams is None:
        acausal_diagrams = {}
    # this data is retained for use in the next model traversal.
    blocks = {}  # dict{acausal_block_uuid:block_spec}
    acausal_links = {}  # links between two acausal ports
    causal_inlinks = {}  # links between causal_block and actuator_causal_port
    causal_outlinks = {}  # links between sensor_causal_port and causal_block

    # this data is only used here locally, and tossed on departure.
    phleaf_input_ui_ids = {}  # dict{block_ui_id:list(port_idx)}
    phleaf_output_ui_ids = {}  # dict{block_ui_id:list(port_idx)}
    block_uuid_to_name = {}

    for block_spec in diagram.nodes:
        # block names are used as locally (in this canvas) unique identifiers
        block_name = block_spec.name
        block_ui_id = block_spec.uuid
        block_uuid_to_name[block_ui_id] = block_name

        # these are used for rich errors before the block is created
        block_name_path = parent_path + [block_name]
        block_ui_id_path = parent_ui_id_path + [block_ui_id]

        # branche for recursing into subdiagrams
        if block_spec.type == "core.ReferenceSubmodel":
            # FIXME: not searching for acausal diagrams under any submodels.
            continue
        elif block_spec.type in (
            "core.Group",
            "core.Submodel",
        ):
            acausal_diagrams = identify_acausal_networks(
                name=block_name,
                diagram=subdiagrams.get_diagram(block_spec.uuid),
                subdiagrams=subdiagrams,
                parent_path=block_name_path,
                parent_ui_id_path=block_ui_id_path,
                ui_id=block_ui_id,
                acausal_diagrams=acausal_diagrams,
            )

        # branch for identifying acausal component blocks
        elif block_spec.type[0:5] == "phys.":
            # FIXME: the above condition is terrible
            blocks[block_ui_id] = block_spec
            # print(f"phys block inputs: {block_spec.inputs}")
            if block_spec.inputs:
                for idx, ioport in enumerate(block_spec.inputs):
                    # FIXME, we need a more explicit way to identify explicit ports of acausal blocks
                    if ioport.variant.variant_kind is None:
                        if block_ui_id not in phleaf_input_ui_ids.keys():
                            phleaf_input_ui_ids[block_ui_id] = []
                        port_ids = phleaf_input_ui_ids[block_ui_id]
                        port_ids.append(idx)
                        phleaf_input_ui_ids[block_ui_id] = port_ids

            # print(f"phys block outputs: {block_spec.outputs}")
            if block_spec.outputs:
                for idx, ioport in enumerate(block_spec.outputs):
                    # FIXME, we need a more explicit way to identify explicit ports of acausal blocks
                    if ioport.variant.variant_kind is None:
                        if block_ui_id not in phleaf_output_ui_ids.keys():
                            phleaf_output_ui_ids[block_ui_id] = []
                        port_ids = phleaf_output_ui_ids[block_ui_id]
                        port_ids.append(idx)
                        phleaf_output_ui_ids[block_ui_id] = port_ids

    phleaf_block_ui_ids = set(blocks.keys())
    for link in diagram.links:
        if (
            (link.src is None)
            or (link.dst is None)
            or (link.src.node not in block_uuid_to_name)
            or (link.dst.node not in block_uuid_to_name)
        ):
            continue

        src_block_name = block_uuid_to_name[link.src.node]
        dst_block_name = block_uuid_to_name[link.dst.node]
        src_port_index = int(link.src.port)
        dst_port_index = int(link.dst.port)

        node_ui_id_set = set([link.src.node, link.dst.node])
        # when the dst of a link is a block in the phleaf network, this is a phleaf
        # input, and vice versa for output.
        is_phleaf_input = False
        is_phleaf_output = False
        if link.dst.node in phleaf_input_ui_ids.keys():
            if dst_port_index in phleaf_input_ui_ids[link.dst.node]:
                is_phleaf_input = True
        elif link.src.node in phleaf_output_ui_ids.keys():
            if src_port_index in phleaf_output_ui_ids[link.src.node]:
                is_phleaf_output = True

        if is_phleaf_output and is_phleaf_input:
            raise NotImplementedError(
                f"Direct causal connections between acausal sensors and actuators is not supported."
                f"Offending blocks: {src_block_name}, {dst_block_name}"
            )

        if (
            node_ui_id_set.issubset(phleaf_block_ui_ids)
            and not is_phleaf_input
            and not is_phleaf_output
        ):
            # when both src and dst blocks are blocks in the physical network, and neither
            # has been identified as an explicit connection to the physical network, this
            # means this link is between two acausal ports.
            acausal_links[link.uuid] = link
        elif is_phleaf_input and link.src.node not in blocks.keys():
            # dst node is a phleaf actuator block, and the other is not an acasual block.
            # this case can only be a causal input to the phleaf.
            causal_inlinks[link.uuid] = link
        elif is_phleaf_output and link.dst.node not in blocks.keys():
            # src node is a phleaf sensor block, and the other is not an acasual block.
            # this case can only be a causal output from the phleaf.
            causal_outlinks[link.uuid] = link

    if blocks:
        acausal_diagram = AcausalDiagram(
            blocks=blocks,
            acausal_links=acausal_links,
            causal_inlinks=causal_inlinks,
            causal_outlinks=causal_outlinks,
        )
        parent_ui_id_path_str = ".".join(parent_ui_id_path)
        acausal_diagrams[parent_ui_id_path_str] = acausal_diagram

    return acausal_diagrams


def build_acausal_network(
    acausal_diagram: AcausalDiagram,
    namespace_params,
    name: str,
    parent_path: list[str],
    parent_ui_id_path: list[str],
) -> (LeafSystem, dict, dict):
    """
    this builds a network object using the data for blocks and links that was collected
    for the phleaf during the model traversal in identify_acausal_networks().
    """
    blocks = acausal_diagram.blocks
    links = acausal_diagram.acausal_links
    causal_inlinks = acausal_diagram.causal_inlinks
    causal_outlinks = acausal_diagram.causal_outlinks

    # create acausal component objects from block_specs
    uuid_to_comp = {}
    for block_spec in blocks.values():
        block_name_path = parent_path + [block_spec.name]
        block_ui_id_path = parent_ui_id_path + [block_spec.uuid]
        common_kwargs = {"name": block_spec.name}
        parameters = eval_parameters(
            instance_parameters=block_spec.parameters,
            call_site_namespace=namespace_params,
            name_path=block_name_path,
            ui_id_path=block_ui_id_path,
        )
        comp = block_interface.get_block_fcn(block_spec.type)(
            block_spec=block_spec,
            **common_kwargs,
            **parameters,
        )
        uuid_to_comp[block_spec.uuid] = comp

    # create acausal Network object
    nw = Network(name=name, comp_list=uuid_to_comp.values())

    # define connections in the acasual network
    for link_uuid, link in links.items():
        cmp_a = uuid_to_comp[link.src.node]
        cmp_b = uuid_to_comp[link.dst.node]

        src_port_index = int(link.src.port)
        dst_port_index = int(link.dst.port)

        # FIXME: this is a wicked nasty hack
        # acausal components ports should really be referred to by name, but json
        # links refer to ports by src/dst+index. acausal components do not have src/dst,
        # so to differentiate here we make dst index negative, that way components can
        # use the index only to know which port is connected.
        # as such, we have to index starting at one because we cant differentiate between
        # 0 and -0.
        cmp_a_port_idx = src_port_index + 1
        cmp_b_port_idx = (dst_port_index + 1) * -1
        port_a = cmp_a.port_idx_to_name[cmp_a_port_idx]
        port_b = cmp_b.port_idx_to_name[cmp_b_port_idx]
        nw.connect(cmp_a, port_a, cmp_b, port_b)

    # create an acausal compiler object, and generate the phleaf
    AcausalCompiler = Compiler(nw)
    phleaf, insym_to_portid, outsym_to_portid = AcausalCompiler.generate_phleaf(
        name=name
    )

    # create link end point remapping data so that when back in the causal diagram assembly,
    # we can remap link end points to phleaf ports instead of the acausal block ports.
    inlinks_map = {}
    for link_uuid, link in causal_inlinks.items():
        cmp = uuid_to_comp[link.dst.node]
        sym = cmp.get_in_sym()
        phleaf_portid = insym_to_portid[sym]
        inlinks_map[link.dst.node] = {int(link.dst.port): phleaf_portid}

    outlinks_map = {}
    for link_uuid, link in causal_outlinks.items():
        cmp = uuid_to_comp[link.src.node]
        sym = cmp.get_out_sym()
        phleaf_portid = outsym_to_portid[sym]
        outlinks_map[link.src.node] = {int(link.src.port): phleaf_portid}

    return phleaf, inlinks_map, outlinks_map


def simulation_settings(
    config: model_json.Configuration, recorded_signals: dict[str, SystemCallback] = None
):
    sim_output_mode_lookup = {
        "auto": ResultsMode.auto,
        "discrete_steps_only": ResultsMode.discrete_steps_only,
        "fixed_interval": ResultsMode.fixed_interval,
    }
    sim_output_mode = sim_output_mode_lookup.get(
        config.sim_output_mode, ResultsMode.auto
    )

    method = config.solver.method
    if method in ["default", "non-stiff"]:
        pass
    elif method in ["RK45"]:
        method = "non-stiff"
    elif method in ["stiff", "BDF", "Kvaerno5"]:
        method = "stiff"
    else:
        raise ValueError(f"Unsupported solver method: {config.solver.method}")

    numerical_backend = config.numerical_backend or "auto"
    if numerical_backend not in ["auto", "numpy", "jax"]:
        raise ValueError(f"Unsupported numerical backend: {config.numerical_backend}")

    results_options = ResultsOptions(
        mode=sim_output_mode,
        max_results_interval=config.max_results_interval,
        fixed_results_interval=config.fixed_results_interval,
    )

    simulator_options = SimulatorOptions(
        math_backend=numerical_backend,
        max_major_steps=config.max_major_steps,
        max_major_step_length=config.sample_time,
        min_minor_step_size=config.solver.min_step,
        max_minor_step_size=config.solver.max_step,
        atol=config.solver.absolute_tolerance,
        rtol=config.solver.relative_tolerance,
        ode_solver_method=method,
        return_context=False,
        recorded_signals=recorded_signals,
    )

    logging.info("Simulation settings: %s", simulator_options)
    logging.info("Results settings: %s", results_options)

    return results_options, simulator_options
