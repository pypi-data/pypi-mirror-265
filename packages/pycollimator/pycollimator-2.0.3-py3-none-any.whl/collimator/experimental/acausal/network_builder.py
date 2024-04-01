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

from .component_library.base import sym


class Network:
    # FIXME: needs a better name
    """
    collection of components and connections representing a network of acausal components.
    """

    def __init__(self, name=None, comp_list=None, cnctn_list=None):
        self.name = "sys" if name is None else name
        self.comps = set() if comp_list is None else set(comp_list)
        self.connections = [] if cnctn_list is None else cnctn_list
        self.t_sym = sym("t", kind="var")  # symbol for time (independent variable)
        self.syms = set()
        self.eqs = set()  # accumulate equations, and remove

    # TODO:
    # 1] verify that each connection is between 2 ports of the same domain
    # 2] find a way to spread not-None IC of node state to other equivalent states of
    # same node whose ICs are None

    def connect(self, cmp_a, port_a, cmp_b, port_b):
        # add the components
        self.comps.update(set([cmp_a, cmp_b]))

        # add the symbols from each component
        self.syms.update(cmp_a.syms)
        self.syms.update(cmp_b.syms)

        # add the equations from the components
        self.eqs.update(cmp_a.eqs)
        self.eqs.update(cmp_b.eqs)

        # add the connection between the components
        self.connections.append(((cmp_a, port_a), (cmp_b, port_b)))

    @property
    def input_syms(self):
        syms = []
        for comp in self.comps:
            sym = comp.get_in_sym()
            if sym is not None:
                syms.append(sym)
        return syms

    @property
    def num_inputs(self):
        return len(self.input_syms)

    @property
    def has_inputs(self):
        return self.num_inputs > 0

    @property
    def output_syms(self):
        syms = []
        for comp in self.comps:
            sym = comp.get_out_sym()
            if sym is not None:
                syms.append(sym)
        return syms

    @property
    def num_outputs(self):
        return len(self.output_syms)

    @property
    def has_outputs(self):
        return self.num_outputs > 0
