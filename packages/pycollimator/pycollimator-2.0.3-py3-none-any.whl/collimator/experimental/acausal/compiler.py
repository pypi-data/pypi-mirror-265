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

import numpy as np
from scipy.integrate import solve_ivp
import copy
import sympy
from sympy import lambdify, solve, Symbol, Eq
from .component_library.base import eqn

# collimator imports
# from collimator.library import *
from collimator.framework import LeafSystem, DependencyTicket
from collimator.backend import numpy_api as cnp


class Compiler:
    # FIXME: needs a better name
    """
    this class does the equation solving to produce the RHS for the system.
    this class also has a *solve* method for systems resulting in ODEs.
    this is not scalable. only the make_node_sets() and add_node_eqs() can
    be used going forward.
    """

    def __init__(self, model):
        self.model = model
        # temporary break out model fields to how they were before Model/Compiler split.
        # eventually these fields should remain in the self.model field.
        self.comps = model.comps
        self.connections = model.connections
        self.t_sym = model.t_sym
        self.syms = model.syms
        self.eqs_all = model.eqs  # accumulate equations, and never remove
        self.name = model.name

        # fields unique to Compiler class
        # self.syms = set()
        self.syms_map = {}  # dict mapping sympy symbol to it parent 'sym' object.
        self.eqs_rhs = set()  # accumulate equations, and remove
        self.eqs_outputs = set()  # accumulate equations, and remove
        self.nodes = {}  # dict of node_id to set of ports
        self.pot_master_to_slave_map = {}  # for debugging
        self.pot_slave_to_master_map = {}  # map from slave pot to its master
        self.rhs_exprs = {}  # dict from st_sym to an expression for its derivative.
        self.output_exprs = {}  # dict from output_sym to an expression for it.
        self.st_ic = {}  # dict from state symbol to state initial condition
        self.params = {}  # dict from param symbol to param value
        self.inputs = []  # list of input sym object
        self.preamble_done = False
        self.incidence_matrix = None

    # TODO:
    # 1] find a way to spread not-None IC of node state to other equivalent states of
    # same node whose ICs are None

    def pp_eqs(self, eqs_all=False):
        eqs = self.eqs_all if eqs_all else self.eqs_rhs
        print(f"len_eqs={len(eqs)}")
        for eq in eqs:
            print(f"\t{eq}")

    def sanitize_solve(self, s, expr):
        # helper function.
        # handle the various options for what can be returned from solve().
        if isinstance(expr, list):
            if len(expr) > 1:
                raise RuntimeError(
                    f"solving {expr} for {s} produced more than one solution."
                )
            elif len(expr) == 0:
                raise RuntimeError(f"solving {expr} for {s} produced no solutions.")
            else:
                return expr[0]
        else:
            # @am. its not clear whether 'not a list' is an acceptable outcome,
            # so block it for now.
            print(f"sanitize_solve failed: s={s}, expr={expr}")
            raise RuntimeError("sanitize_solve expr arg is not a list.")

    # processing of system of equations starts here.
    def make_node_sets(self):
        """
        naive algorithm to sort port-pairs into sets of ports belonging to a node in the model.
        start by assuming each port-pair is its own node, i.e. a model with components connected in a line.
        intialize a dict 'nodes' by enumerating each of these into a dict{1:set1,2:set2, ...etc.}
        initial 'workset' as a list nodes.keys(), e.g. a list fo all the node IDs.
        then, pop an ID from workset, and pop the corresponding node(N) from 'nodes'.
            check if any other node shares a port with N,
                if say node M shares a port with N, merge all ports of node N into node M, leaving M in 'nodes'.
                if no other nodes share a port with N, re-add N to workset, because it is a complete node.
        if workset empty, we are done.
        """
        # print("Compiler.make_node_sets()")
        nodes = {id: set(port_pair) for id, port_pair in enumerate(self.connections)}
        workset = list(nodes.keys())
        while workset:
            this_id = workset.pop()
            this_port_set = nodes.pop(this_id)
            # print(f'this_id={this_id}, this_port_set={this_port_set}, workset={workset}')
            this_set_grouped = False
            for idx, port_set in nodes.items():
                if not port_set.isdisjoint(this_port_set):
                    nodes[idx].update(this_port_set)
                    this_set_grouped = True

            if not this_set_grouped:
                nodes[this_id] = this_port_set

        self.nodes = nodes

    def add_node_eqs(self):
        """
        for each node in the system, generate the flow and potential equations.
        also generate the maps between master and slave potential variables used in substitution.
        also generate maps between potential variables and their initial conditions.
        """

        # print("Compiler.add_node_eqs()")
        for node_id, port_set in self.nodes.items():
            # print(f"\nnode_id={node_id}")
            flow_syms_on_node = set()
            master_pot = None
            for port_tuple in port_set:
                cmp, port_id = port_tuple
                port = cmp.ports[port_id]
                # print(f"port={port}")

                # collect the flow symbols to create balancing equation for node
                if port.flow is not None:
                    flow_syms_on_node.add(port.flow.s)

                # chose a master potential variable for the node, and make the associations between master and slaves
                if port.pot is not None:
                    if master_pot is None:
                        master_pot = port.pot
                        # print(f"master_pot={master_pot}. port.pot.s={port.pot.s}")
                        self.pot_master_to_slave_map[master_pot.s] = set()
                        if master_pot.d is not None:
                            self.pot_master_to_slave_map[master_pot.d] = set()

                    else:
                        # add pot slave to maps, and create equation
                        self.pot_master_to_slave_map[master_pot.s].add(port.pot.s)
                        self.pot_slave_to_master_map[port.pot.s] = master_pot.s

                        # FIXME: are these 'pot' eqs ever used? maybe for creating the output function?
                        # I ask because we sort of make them implicitly with pot_slave_to_master_map
                        self.eqs_all.add(
                            eqn(
                                e=Eq(port.pot.s, master_pot.s),
                                kind="pot",
                                node_id=node_id,
                            )
                        )

                        if master_pot.d is not None and port.pot.d is not None:
                            # add der(pot) slave to maps, if it exists
                            self.pot_master_to_slave_map[master_pot.d].add(port.pot.d)
                            self.pot_slave_to_master_map[port.pot.d] = master_pot.d
                            # create equation. @am. we actually dont want to do this.
                            # self.eqs_all.add(eqn(e=Eq(port.pot.d,master_pot.d),node_id=node_id))

            # create and save the balancing equation for the node
            sum_expr = sympy.core.add.Add(*flow_syms_on_node)
            # print(f'sum_expr {sum_expr}')
            self.eqs_all.add(eqn(e=Eq(0, sum_expr), kind="flow", node_id=node_id))

        self.eqs_rhs = copy.deepcopy(self.eqs_all)
        # self.pp_eqs(eqs_all=True)

    def var_subs_pot(self):
        """
        perform symbolic substitutions to remove:
            slave potential variables

        any time a variable is replace by substitution of an expr
        where the expr was found by solving an equation for the variable,
        the equation should be removed from the equation set since its
        relation is now encoded in the remaining equations.
        e.g. one variable removed, one equation removed.
        """
        # print("Compiler.var_subs_pots()")
        # perform the potential variable substitutions in the all equations.
        # must perform this step before flow substitutions.
        # print(f"eqs before remove pot eqs")
        # self.pp_eqs()
        self.eqs_rhs = set([eq for eq in self.eqs_rhs if eq.kind != "pot"])

        # print(f"eqs before pot subs")
        # self.pp_eqs()

        for slave_pot, master_pot in self.pot_slave_to_master_map.items():
            # print(f"\nmaster_pot:{master_pot}. slave_pot:{slave_pot}")
            self.eqs_rhs = set([eq.subs(slave_pot, master_pot) for eq in self.eqs_rhs])

        # print(f"eqs after pot subs")
        # self.pp_eqs()

    def var_subs_flow(self):
        """
        perform symbolic substitutions to remove:
            flow variables

        any time a variable is replace by substitution of an expr
        where the expr was found by solving an equation for the variable,
        the equation should be removed from the equation set since its
        relation is now encoded in the remaining equations.
        e.g. one variable removed, one equation removed.
        """
        # print("Compiler.var_subs_flow()")
        # perform the flow variable substitutions in the appropriate equations.
        disconnected_flow_vars = set()
        for s in self.syms:
            if s.kind == "flow":
                # print(f"\nfound flow sym:{s.name}")

                # find an equation that can be used to get an expression for 's'
                sub_expr = None
                for eq in self.eqs_rhs:
                    # print(f"eq:{eq}")
                    eq_syms = eq.e.atoms(Symbol)
                    if s.s in eq_syms and sub_expr is None:
                        sub_exprs = solve(eq.e, s.s)
                        # TODO: need to implement some kind of check/validation that this
                        # solve operation resulted in the desired outcome. I dont presently
                        # know what this means, but i suspect there are scenarios where
                        # this naive solve() doesn't produce the desired outcome, and for
                        # example, it may be better to just move onto the next equation.
                        # presently, i dont know what the rules are for making this decision
                        # some ideas:
                        # 1] if len(sub_expr) > 1. in this case it may be ambiguous which
                        # solution to pick, but it may be that either is fine. it's not
                        # clear to me yet, so do not accept this case as valid for now.
                        # 2] if len(sub_expr) == 0, then solve failed, so clearly this means
                        #  move onto the next equation.

                        if len(sub_exprs) == 1:  # this implements ideas 1&2 from above.
                            # if an equation E has been used as a substitution expression for a
                            # 'flow' variable A, we have to remove E from the set of equations
                            # because E is being substituted inside the other equations.
                            # keeping E in the set would mean we could get a sub_expr for another
                            # 'flow' variable B, and this sub_expr would be in terms of A,
                            # and we would just re-introduce A when the whole point was to
                            # eliminate A from all equations in the set.
                            sub_expr = sub_exprs[0]
                            # print(f"sub_expr:{sub_expr}")
                            remove_eq = eq
                            break  # once we found a substitution, we dont need to look further

                if sub_expr is None:
                    # it is imperative that we find a sub_expr for each 'flow' variable.
                    # otherwise the system is indeterminate.
                    raise Exception(
                        f"could not find a sub_expr for flow variable {s.name}. system may have more variables than equations"
                    )

                # we solved an equation, and will use it to perform substitutions to reomve
                # variable form the system, this means the equation must also be removed from
                # the system
                self.eqs_rhs.remove(remove_eq)

                # we need to immediately perform the substitution in all possible places
                # to prevent var we want to eliminate from leaking past this substitution
                # opertaion.
                # self.eqs_rhs = set([eq.subs(s.s, sub_expr) for eq in self.eqs_rhs])
                replace_cnt = 0
                for eq in self.eqs_rhs:
                    eq_syms_ = eq.e.atoms()
                    if s.s in eq_syms_:
                        replace_cnt = replace_cnt + 1
                if replace_cnt > 0:
                    self.eqs_rhs = set([eq.subs(s.s, sub_expr) for eq in self.eqs_rhs])
                else:
                    print(
                        f'f"no substitution options for flow var {s} with sub_expr {sub_expr}"'
                    )
                    # raise RuntimeError(
                    #     f"no substitution options for flow var {s} with sub_expr {sub_expr}"
                    # )
                    disconnected_flow_vars.add(s)

                # print(f"eqs after replace flow var {s.s} with sub_expr {sub_expr}:")
                # self.pp_eqs()

        # print(f"disconnected_flow_vars={disconnected_flow_vars}")
        self.eqs_outputs = copy.deepcopy(self.eqs_rhs)

    def compute_rhs_symbolic(self):
        # print("Compiler.compute_rhs_symbolic()")
        self.syms_map = {v.s: v for v in self.syms}

        # print("collect the symbols for the states")
        # collect the symbols for the states, and the symbols for their derivatives
        # NOTE: it is imerative that flow and pot(master,slave) substitutios happen before this step.
        st_syms_with_rhs = set()
        st_syms_all = set()
        der_sym_to_rhs = {}
        st_sym_to_der_sym = {}
        intermediate_st_syms = set()
        slave_states_to_der_sym = {}
        for s in self.syms:
            if s.d is not None:  # this means the symbol has a derivative symbol
                # print(f"\nst sym={s}")
                st_syms_all.add(s)  # and hence it is 'a state' of the system
                der_sym = s.d  # useless var remapping. could just use s.d every below.

                st_sym_to_der_sym[s] = der_sym
                der_sym_obj = self.syms_map[der_sym]
                # print(f"der_sym_obj.d={der_sym_obj.d}")
                if der_sym_obj.d is not None:
                    # intermediate states RHS is just the state variable for it's derivative.
                    # it is imperative that they appear in the RHS equation like:
                    #   der(intermediate_state) = intermediate_state_derivative_symbol
                    # as such, with highest priority, we wnat to classify states as
                    # intermediate, such that dont we dont attempt to have them appears
                    # in the RHS equation any othe way.
                    intermediate_st_syms.add(s)
                    # print(f"found intermediate state:{s.name}")
                    # st_syms_with_rhs.add(der_sym_obj)  # @am. this may be futile.
                elif s.d in self.pot_slave_to_master_map.keys():
                    # print(f"found slave state:{s.name}")
                    slave_states_to_der_sym[s] = self.pot_slave_to_master_map[s.d]
                else:
                    # print(f"found state with rhs_expr:{s.name}: der_sym:{der_sym}")
                    st_syms_with_rhs.add(s)

        # print(f"\nst_syms_with_rhs:{st_syms_with_rhs}")
        # print(f"slave_states_to_der_sym:{slave_states_to_der_sym}")
        # print(f"intermediate_st_syms:{intermediate_st_syms}\n")

        # der_sym_replacers = {}
        # der_sym_replacees = {}
        for s in st_syms_with_rhs:
            der_sym = st_sym_to_der_sym[s]
            # now use the equations to try to get an expression for the RHS
            error_no_rhs = True
            for eq in self.eqs_rhs:
                if eq.kind != "pot":
                    eq_syms = eq.e.atoms(Symbol)
                    # print(f"eq={eq}, eq_syms={eq_syms}, der_sym={der_sym}")
                    # FIXME: this may not scale well.
                    if der_sym in eq_syms:
                        # FIXME: i think more checks are needed before the result can
                        # just be used like this.

                        rhs_expr = solve(eq.e, der_sym)
                        rhs_expr = self.sanitize_solve(der_sym, rhs_expr)

                        # print(f"\tder({s})={rhs_expr} from {eq}")
                        error_no_rhs = False

                        # we solved an equation, and will use it to perform substitutions to reomve a
                        # variable from the system, this means the equation must also be removed from
                        # the system.
                        self.eqs_rhs.remove(eq)

                        # we need to immediately perform the substitution in all possible places
                        # to prevent the var we want to eliminate from leaking past this substitution
                        # opertaion.
                        # sub in self.eqs_rhs
                        self.eqs_rhs = set(
                            eq_.subs(der_sym, rhs_expr) for eq_ in self.eqs_rhs
                        )
                        # sub in already collected RHS expressions
                        for st_sym, other_rhs_expr in self.rhs_exprs.items():
                            self.rhs_exprs[st_sym] = other_rhs_expr.subs(
                                der_sym, rhs_expr
                            )
                        # sub in already collected RHS expressions
                        for other_der_sym, other_rhs_expr in der_sym_to_rhs.items():
                            der_sym_to_rhs[other_der_sym] = other_rhs_expr.subs(
                                der_sym, rhs_expr
                            )

                        # update the maps before mobving onto to next state symbol
                        self.rhs_exprs[s] = rhs_expr
                        der_sym_to_rhs[der_sym] = rhs_expr

                        break

            if error_no_rhs:
                raise RuntimeError(
                    f"{s} should have rhs in the equations, but none found."
                )

        # print(f"\nrhs_exprs_symbolic so far:")
        # for s, rhs_expr in self.rhs_exprs.items():
        #     print(f"\tder({s})={rhs_expr}")

        # for the remaining states, there is no expr in the equations for their derivative.
        # i.e. their derivative did not appear in any equations.
        # these states *must* rely on another state as their derivative.
        # e.g. position relies on velocity state as the expr for its derivative. dxdt=v
        # print(f"\nrhs_exprs for remaining states:")
        for slave_st, der_sym in slave_states_to_der_sym.items():
            self.rhs_exprs[slave_st] = der_sym_to_rhs[der_sym]

        for s in intermediate_st_syms:
            self.rhs_exprs[s] = s.d

        # print(f"rhs_exprs final:")
        # for s, rhs_expr in self.rhs_exprs.items():
        #     print(f"\tder({s})={rhs_expr}")

    def remove_not_st_nor_param_vars(self):
        """
        the RHS of any state must only contain symbols for states and parameters.
        no other symbols have defined numerical meaning.
        therefore we need to remove any remaining potential vairables which are
        not states by iterative substitution using the remaining equations.
        """
        # print("Compiler.remove_not_st_nor_param_vars()")

        def get_syms_to_remove(self):
            # get all unique symbols in all RHSs
            all_rhs_syms = set()
            for st_sym, rhs_ in self.rhs_exprs.items():
                rhs_syms = rhs_.atoms(Symbol)
                all_rhs_syms.update(set(rhs_syms))

            syms_to_remove = []
            for s in all_rhs_syms:
                ss = self.syms_map[s]
                if ss not in self.rhs_exprs.keys() and ss.kind not in [
                    "in",
                    "param",
                ]:
                    # @am. do we want to keep a list of sym() objects, as opposed to
                    # the list of sympy symbols as is done here?
                    syms_to_remove.append(s)

            return syms_to_remove

        syms_to_remove = get_syms_to_remove(self)

        pot_sub_exprs = {}
        # print(f"syms_to_remove={syms_to_remove}")
        while_cnt = 0
        while_cnt_limit = 20
        while syms_to_remove:
            if while_cnt >= while_cnt_limit:
                raise RuntimeError(
                    "remove_not_st_nor_param_vars() exceeded while loop development limit."
                )
            # print(f"\nwhile_cnt={while_cnt}. syms_to_remove={syms_to_remove}")
            sym_to_remove = syms_to_remove.pop()
            # print(f"rhs_exprs:")
            # for pp_st, pp_rhs in self.rhs_exprs.items():
            #     print(f"\tder({pp_st})={pp_rhs}")
            # print(f"{sym_to_remove} not a state nor a param. remove by substitution")
            # this symbol cannot stay in the RHS, must be replaced by sustitution
            found_sub_expr = False
            for eq in self.eqs_rhs:
                eq_syms = eq.e.atoms(Symbol)
                if sym_to_remove in eq_syms:
                    sub_expr = solve(eq.e, sym_to_remove)
                    sub_expr = self.sanitize_solve(sym_to_remove, sub_expr)
                    # print(f"found {sym_to_remove} in {eq}. sub_expr={sub_expr}")
                    found_sub_expr = True
                    pot_sub_exprs[sym_to_remove] = sub_expr
                    # once used for substitution, the equation must be remove.
                    self.eqs_rhs.remove(eq)

                    # perform the substitution in the RHS expressions
                    for der_sym, rhs_expr in self.rhs_exprs.items():
                        new_rhs_expr = rhs_expr.subs(sym_to_remove, sub_expr)
                        self.rhs_exprs[der_sym] = new_rhs_expr

                    # perform the substitutions in the remaining equations since the
                    # sym_to_remove should no longer appear in any equations, or else
                    # it might reappear in a sub_expr for a future sym_to_remove
                    self.eqs_rhs = set(
                        [eq.subs(sym_to_remove, sub_expr) for eq in self.eqs_rhs]
                    )

                    break

            if not found_sub_expr:
                raise RuntimeError(
                    f"cound not find a sub_expr for symbol {sym_to_remove}"
                )

            syms_to_remove = get_syms_to_remove(self)
            # print(f"syms_to_remove={syms_to_remove}")
            while_cnt = while_cnt + 1

        # print(f"pot_sub_exprs={pot_sub_exprs}")

    def compute_outputs_symbolic(self):
        # print("Compiler.compute_outputs_symbolic()")
        self.syms_map = {v.s: v for v in self.syms}

        # print("collect the symbols for the states")
        # collect the symbols for the states, and the symbols for their derivatives
        # NOTE: it is imerative that flow and pot(master,slave) substitutios happen before this step.
        output_syms = set()
        out_sym_to_rhs = {}
        for s in self.syms:
            # print(f"s={s} s.kind={s.kind}")
            if s.kind == "out":
                output_syms.add(s)
        # print(f"output_syms={output_syms}")
        for s in output_syms:
            # print(f"output_sym={s}")
            out_sym = s.s
            # now use the equations to try to get an expression for the output
            error_no_expr = True
            for eq in self.eqs_outputs:
                eq_syms = eq.e.atoms(Symbol)
                # print(f"eq={eq}, eq_syms={eq_syms}, out_sym={out_sym}")
                if out_sym in eq_syms:
                    out_expr = solve(eq.e, out_sym)
                    out_expr = self.sanitize_solve(out_sym, out_expr)

                    # print(f"\t{s}={out_expr} from {eq}")
                    error_no_expr = False

                    # we solved an equation, and will use it to perform substitutions to reomve a
                    # variable from the system, this means the equation must also be removed from
                    # the system.
                    self.eqs_outputs.remove(eq)

                    # we need to immediately perform the substitution in all possible places
                    # to prevent the var we want to eliminate from leaking past this substitution
                    # opertaion.
                    # sub in self.eqs_outputs
                    self.eqs_outputs = set(
                        eq_.subs(out_sym, out_expr) for eq_ in self.eqs_outputs
                    )

                    self.output_exprs[s] = out_expr
                    out_sym_to_rhs[out_sym] = out_expr

                    break

            if error_no_expr:
                raise RuntimeError(
                    f"{s} should have expression in the equations, but none found."
                )

    def remove_not_st_nor_param_vars_output(self):
        """
        the expr of any output must only contain symbols for states, inputs, parameters.
        no other symbols have defined numerical meaning.
        therefore we need to remove any remaining potential vairables which are
        not states by iterative substitution using the remaining equations.
        """
        # print("Compiler.remove_not_st_nor_param_vars_output()")

        def get_syms_to_remove(self):
            # get all unique symbols in all output exprs
            all_output_syms = set()
            for output_sym, expr_ in self.output_exprs.items():
                output_syms = expr_.atoms(Symbol)
                all_output_syms.update(set(output_syms))

            syms_to_remove = []
            for s in all_output_syms:
                ss = self.syms_map[s]
                if ss not in self.rhs_exprs.keys() and ss.kind not in [
                    "in",
                    "param",
                ]:
                    # @am. do we want to keep a list of sym() objects, as opposed to
                    # the list of sympy symbols as is done here?
                    syms_to_remove.append(s)

            return syms_to_remove

        syms_to_remove = get_syms_to_remove(self)

        pot_sub_exprs = {}
        # print(f"syms_to_remove={syms_to_remove}")
        while_cnt = 0
        while_cnt_limit = 20
        while syms_to_remove:
            if while_cnt >= while_cnt_limit:
                raise RuntimeError(
                    "remove_not_st_nor_param_vars() exceeded while loop development limit."
                )
            # print(f"\nwhile_cnt={while_cnt}. syms_to_remove={syms_to_remove}")
            sym_to_remove = syms_to_remove.pop()
            # print(f"rhs_exprs:")
            # for pp_st, pp_rhs in self.rhs_exprs.items():
            #     print(f"\tder({pp_st})={pp_rhs}")
            # print(f"{sym_to_remove} not a state nor a param. remove by substitution")
            # this symbol cannot stay in the RHS, must be replaced by sustitution
            found_sub_expr = False
            for eq in self.eqs_outputs:
                eq_syms = eq.e.atoms(Symbol)
                if sym_to_remove in eq_syms:
                    sub_expr = solve(eq.e, sym_to_remove)
                    sub_expr = self.sanitize_solve(sym_to_remove, sub_expr)
                    # print(f"found {sym_to_remove} in {eq}. sub_expr={sub_expr}")
                    found_sub_expr = True
                    pot_sub_exprs[sym_to_remove] = sub_expr
                    # once used for substitution, the equation must be remove.
                    self.eqs_outputs.remove(eq)

                    # perform the substitution in the output expressions
                    for out_sym, output_expr in self.output_exprs.items():
                        new_output_expr = output_expr.subs(sym_to_remove, sub_expr)
                        self.output_exprs[out_sym] = new_output_expr

                    # perform the substitutions in the remaining equations since the
                    # sym_to_remove should no longer appear in any equations, or else
                    # it might reappear in a sub_expr for a future sym_to_remove
                    self.eqs_outputs = set(
                        [eq.subs(sym_to_remove, sub_expr) for eq in self.eqs_outputs]
                    )

                    break

            if not found_sub_expr:
                raise RuntimeError(
                    f"cound not find a sub_expr for symbol {sym_to_remove}"
                )

            syms_to_remove = get_syms_to_remove(self)
            # print(f"syms_to_remove={syms_to_remove}")
            while_cnt = while_cnt + 1

        # print(f"pot_sub_exprs={pot_sub_exprs}")

    def get_params_ic(self):
        # print("Compiler.get_params_ic()")
        for sym in self.syms:
            if sym.ic is not None:
                self.st_ic[sym] = sym.ic
            if sym.kind == "param":
                self.params[sym] = sym.val

    # processing ends here

    def simulate_scipy(self, tspan=[0, 10], results_interval=0.01, inputs_fun=None):
        """
        This is a very early stage testing tool that will eventually go away.
        """
        print("Compiler.simulate_scipy()")
        if not self.preamble_done:
            self.preamble()

        # create the lambda function input args vector.
        # [time, states, params, inputs]
        lambda_args = (
            [self.t_sym.s]
            + list(s.s for s in self.rhs_exprs.keys())
            + list(s.s for s in self.params.keys())
            + self.model.input_syms
        )
        # print(f"lambda_args={lambda_args}")

        # create sovle_ivp results evaluation points
        t_eval = np.arange(tspan[0], tspan[1], results_interval)

        # create state vector
        ys = np.zeros(len(self.rhs_exprs.keys()))
        for idx, st_sym in enumerate(self.rhs_exprs.keys()):
            if st_sym in self.st_ic.keys():
                ys[idx] = self.st_ic[st_sym]
        # print(f"ys init={ys}")

        # create params values vector
        ps = np.zeros(len(self.params.keys()))
        for idx, param_sym in enumerate(self.params.keys()):
            if param_sym in self.params.keys():
                ps[idx] = self.params[param_sym]
        # print(f"ps={ps}")

        lambdify_rhs = lambdify(lambda_args, list(self.rhs_exprs.values()), "numpy")

        def scipy_rhs(t, x, *args):
            if inputs_fun is not None:
                inputs = inputs_fun(t)
                return lambdify_rhs(t, *x, *ps, *inputs)
            else:
                return lambdify_rhs(t, *x, *ps)

        sol = solve_ivp(scipy_rhs, tspan, ys, t_eval=t_eval, args=(ps, inputs_fun))

        return sol

    def get_x0_ps(self):
        # create state vector
        ys = np.zeros(len(self.rhs_exprs.keys()))
        for idx, st_sym in enumerate(self.rhs_exprs.keys()):
            if st_sym in self.st_ic.keys():
                ys[idx] = self.st_ic[st_sym]
        # print(f"ys init={ys}")

        # create params values vector
        ps = np.zeros(len(self.params.keys()))
        for idx, param_sym in enumerate(self.params.keys()):
            if param_sym in self.params.keys():
                ps[idx] = self.params[param_sym]
        # print(f"ps={ps}")

        return ys, ps

    def preamble(self, print_step_results=[]):
        if "init" in print_step_results:
            self.pp()

        self.make_node_sets()
        if "make_node_sets" in print_step_results:
            self.pp()

        self.add_node_eqs()
        if "add_node_eqs" in print_step_results:
            self.pp()

        self.var_subs_pot()
        self.var_subs_flow()
        if "var_substitution" in print_step_results:
            self.pp()

        self.compute_rhs_symbolic()
        if "compute_rhs_symbolic" in print_step_results:
            self.pp()

        self.remove_not_st_nor_param_vars()
        if "remove_not_st_nor_param_vars" in print_step_results:
            self.pp()

        self.compute_outputs_symbolic()
        if "compute_outputs_symbolic" in print_step_results:
            self.pp()

        self.remove_not_st_nor_param_vars_output()
        if "remove_not_st_nor_param_vars_output" in print_step_results:
            self.pp()

        self.get_params_ic()
        if "get_params_ic" in print_step_results or "last" in print_step_results:
            self.pp()

        self.preamble_done = True

    def pp(self):
        print(f"Compiler {self.name}:")

        print(f"\tComponents:{[c.name for c in self.comps]}")

        print("\tConnections:")
        for port_tuple_a, port_tuple_b in self.connections:
            ca, pa = port_tuple_a
            cb, pb = port_tuple_b
            print(f"\t\t{ca.name},{pa}\tto {cb.name},{pb}")

        print(f"\tsyms:{self.syms}")

        print(f"\tsyms_map:{self.syms_map}")

        print(f"\teqs: n={len(self.eqs_rhs)}")
        for eq in self.eqs_rhs:
            print(f"\t\t{eq}")

        print(f"\teqs_all: n={len(self.eqs_all)}")
        for eq in self.eqs_all:
            print(f"\t\t{eq}")

        print("\tnode_sets:")
        for id, nset in self.nodes.items():
            if len(nset) > 3:
                print(f"\t\t{id}:")
                for n in nset:
                    print(f"\t\t\t{n}:")
            else:
                print(f"\t\t{id}:{nset}")

        print(f"\tpot_master_to_slave_map:{self.pot_master_to_slave_map}")

        print(f"\tpot_slave_to_master_map:{self.pot_slave_to_master_map}")

        if self.rhs_exprs:
            print("\trhs_exprs_symbolic for all states:")
            for s, rhs_expr in self.rhs_exprs.items():
                print(f"\t\tder({s})={rhs_expr}")

        if self.output_exprs:
            print("\toutput_exprs_symbolic for all outputs:")
            for s, output_expr in self.output_exprs.items():
                print(f"\t\t{s}={output_expr}")

        print(f"\tst_ic={self.st_ic}")
        # print(f"\tlambda_args={self.lambda_args}")
        # print(f"\tsum_forces={self.sum_forces}")

        print(f"end {self.name}\n")

    def generate_phleaf(
        self,
        name="pwrcat",
        leaf_backend="jax",
    ):
        """
        This function is used for generating a phleaf from a AcausalNetwork
        """
        if not self.preamble_done:
            self.preamble()

        # INITIAL STATE AND PARAMETERS
        x0, ps = self.get_x0_ps()

        # LEAF SYSTEM
        phleaf = LeafSystem(name=name)

        # INPUT PORTS
        # this ensure that inports of the phleaf are in the same order as
        # the 'inputs' portion of the lambdify args
        insym_to_portid = {}
        for sym in self.model.input_syms:
            idx = phleaf.declare_input_port(name=sym.name)
            insym_to_portid[sym] = idx

        # COMMON TO ODE AND OUTPUTS
        # create the lambda functions input args vector.
        # [time, states, inputs, params]
        lambda_args = (
            [self.t_sym.s]
            + list(s.s for s in self.rhs_exprs.keys())
            + self.model.input_syms
            + list(s.s for s in self.params.keys())
        )

        # CONTINUOUS STATE AND DYNAMICS
        lambdify_rhs = lambdify(
            lambda_args, list(self.rhs_exprs.values()), leaf_backend
        )

        def _ode(time, state, *inputs):
            cstate = state.continuous_state
            return cnp.array(lambdify_rhs(time, *cstate, *inputs, *ps))

        phleaf.declare_continuous_state(default_value=x0, ode=_ode)

        # OUTPUT PORTS
        outsym_to_portid = {}
        if self.model.num_outputs == 0:
            # if not output, output the state vector
            phleaf.declare_continuous_state_output(name=f"{phleaf.name}:output")
            outsym_to_portid = None
        else:

            def _make_outp_callback2(outp_expr):
                lambdify_output = lambdify(lambda_args, outp_expr, leaf_backend)

                def _output_fun(time, state, *inputs):
                    cstate = state.continuous_state
                    return cnp.array(lambdify_output(time, *cstate, *inputs, *ps))

                return _output_fun

            # declaring phleaf output ports in this order means that the ordering
            # 'source of truth' is self.model.output_syms which can be used to link
            # back to the acausal sensors causal port for diagram link src point remapping.
            for sym in self.model.output_syms:
                outp_expr = self.output_exprs[sym]
                _output = _make_outp_callback2(outp_expr)
                idx = phleaf.declare_output_port(
                    _output,
                    name=sym.name,  # FIXME: not the name from the block port
                    prerequisites_of_calc=[DependencyTicket.xc],
                    requires_inputs=True,
                )
                outsym_to_portid[sym] = idx

        return phleaf, insym_to_portid, outsym_to_portid
