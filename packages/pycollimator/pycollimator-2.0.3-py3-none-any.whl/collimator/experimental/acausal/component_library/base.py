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

from sympy import Symbol


# FIXME: move me to acausal framework?
class sym:
    """
    a class for a symbol that can have an association with the symbol that is it's
    own derivative w.r.t. time.
    This is a work around because sympy doesn't have an internal feature for tracking
    such relationships.
    creation of class means we can track many other attributes of symbols making
    equation manipulation easier and clearer.

    kind qualifies the symbol w.r.t. how it gets treated when rearanging/simplifying
    equations, or determining initial condiitons.
        1] 'flow' means this symbol is a flow variable. it must appear in one and only one
        conservation equation for a given 'node'. e.g. all forces sum to 0.
        2] 'pot' means this symbol is a potential variable. it must appear in at least one
        equality constraint. e.g. all velocities of ports connected to a 'node' must be equal.
        3] 'param' means this symbol is a parameter of the system, e.g. mass, resistance, etc.
        4] 'in' means this symbol is an input, similar to param, but the value is read in
        periodically. e.g. force signal for controlled_ideal_force_source
        5] 'out' means this symbol is a output and therefore must appear on the LHS of an
        expression. e.g. force value for ideal force sensor.
        6] 'var' means this symbol is a variable of the system that does not match any description
        above. e.g. voltage_across_capacitor = capacitor _pot_positive - capacitor _pot_negative, here
        voltage_across_capacitor is a 'var', while the other two are 'pot'.
        similarly, the time derivaive of voltage_across_capacitor would be a 'var'.
    """

    def __init__(self, name, val=None, der_sym=None, kind=None, ic=None):
        supported_kinds = ["flow", "pot", "param", "in", "out", "var"]
        if kind not in supported_kinds:
            raise Exception(
                f"kind:{kind} of symbol:{name} not one of {supported_kinds}"
            )

        if kind == "param" and val is None:
            raise Exception(f"symbol:{name} has kind param, val cannot be None")

        if kind in ["flow", "param", "in", "out"]:
            if ic is not None:
                raise Warning(f"assigning ic to symbol if kind:{kind} has no effect.")

        self.name = name
        self.s = Symbol(name)
        self.d = der_sym
        self.val = val
        self.kind = kind
        self.ic = ic

    def __repr__(self):
        return str(self.s)


# FIXME: move me to acausal framework?
class eqn:
    """
    class for equations and their attributes
    """

    def __init__(self, e, kind=None, node_id=None):
        self.e = e
        self.kind = kind
        self.node_id = node_id  # not user settable. assign by 'interpreter'

    def subs(self, e1, e2):
        # print(f'\t[eqn.subs] eq before {self.e}')
        self.e = self.e.subs(e1, e2)
        # print(f'\t[eqn.subs] eq after  {self.e}')
        return self

    def __repr__(self):
        if self.kind is None:
            return str(self.e)
        else:
            return (
                str(self.e) + ":\t\t\t" + str(self.kind) + "\tnid:" + str(self.node_id)
            )


class PortBase:
    flow = None
    pot = None
    name: str = None

    def __repr__(self):
        return str(
            self.__class__.__name__
            + " pot:"
            + str(self.pot)
            + " flow:"
            + str(self.flow)
        )


class ComponentBase:
    ports = {}
    syms = set()
    eqs = set()

    def __repr__(self):
        return str(self.__class__.__name__ + "_" + self.name)

    def get_in_sym(self):
        # FIXME: does not support component with multiple causal input
        for sym in self.syms:
            if sym.kind == "in":
                return sym
        return None

    def get_out_sym(self):
        # FIXME: does not support component with multiple causal outputs
        for sym in self.syms:
            if sym.kind == "out":
                return sym
        return None
