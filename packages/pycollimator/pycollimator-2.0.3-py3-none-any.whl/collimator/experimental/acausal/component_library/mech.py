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

from sympy import Eq
from .base import sym, eqn, PortBase, ComponentBase


class MechTransPort(PortBase):
    """
    port for a translational mechanical component to interface with others.
    """

    def __init__(self, v_sym=None, f_sym=None):
        self.flow = f_sym
        self.pot = v_sym


class MechTransOnePort(ComponentBase):
    """
    a partial component with one mechanical translational connection.
    """

    def __init__(self, name, v_ic=None, x_ic=None, p="p"):
        self.f = sym(name + "_f", kind="flow")
        self.a = sym(name + "_a", kind="var")
        self.v = sym(name + "_v", kind="pot", der_sym=self.a.s, ic=v_ic)
        self.x = sym(name + "_x", kind="var", der_sym=self.v.s, ic=x_ic)

        self.ports = {p: MechTransPort(v_sym=self.v, f_sym=self.f)}
        self.syms = set([self.f, self.a, self.v, self.x])

        self.port_idx_to_name = {-1: p}


class MechTransTwoPort(ComponentBase):
    """
    a partial component with two mechanical translational connections.
    """

    def __init__(
        self, name, x1_ic=None, v1_ic=None, x2_ic=None, v2_ic=None, p1="p1", p2="p2"
    ):
        self.f1 = sym(self.name + "_f1", kind="flow")
        self.f2 = sym(self.name + "_f2", kind="flow")
        self.a1 = sym(self.name + "_a1", kind="var")
        self.v1 = sym(self.name + "_v1", kind="pot", der_sym=self.a1.s, ic=v1_ic)
        self.x1 = sym(self.name + "_x1", kind="var", der_sym=self.v1.s, ic=x1_ic)
        self.a2 = sym(self.name + "_a2", kind="var")
        self.v2 = sym(self.name + "_v2", kind="pot", der_sym=self.a2.s, ic=v2_ic)
        self.x2 = sym(self.name + "_x2", kind="var", der_sym=self.v2.s, ic=x2_ic)

        self.ports = {
            p1: MechTransPort(v_sym=self.v1, f_sym=self.f1),
            p2: MechTransPort(v_sym=self.v2, f_sym=self.f2),
        }
        self.syms = set(
            [
                self.f1,
                self.f2,
                self.a1,
                self.v1,
                self.x1,
                self.a2,
                self.v2,
                self.x2,
            ]
        )
        self.eqs = set([eqn(e=Eq(0, self.f1.s + self.f2.s))])

        self.port_idx_to_name = {-1: p1, 1: p2}


class MechTransForce(MechTransOnePort):
    """
    ideal force source in mechanical translational domain
    """

    def __init__(self, name=None, force=0.0):
        self.name = "mtf" if name is None else name
        super().__init__(self.name)
        self.fparam = sym(self.name + "_fparam", kind="param", val=force)
        self.syms.add(self.fparam)
        self.eqs = set([eqn(e=Eq(self.fparam.s, self.f.s))])

        # this sucks. need this here because not all one port blocks
        # use the 'input' of the block.
        self.port_idx_to_name = {1: "p"}


class MechTransMass(MechTransOnePort):
    """
    ideal point mass in mechanical translational domain
    """

    def __init__(self, name=None, mass=1.0, v_ic=None, x_ic=None):
        self.name = "mtm" if name is None else name
        super().__init__(self.name, v_ic=v_ic, x_ic=x_ic)

        if mass <= 0.0:
            raise ValueError(
                f"Component {self.__class__.__name__ } {self.name} must have mass>0"
            )

        self.m = sym(self.name + "_m", kind="param", val=mass)
        self.syms.add(self.m)
        self.eqs = set([eqn(e=Eq(self.f.s, self.m.s * self.a.s))])


class MechTransSpring(MechTransTwoPort):
    """
    ideal spring in mechanical translational domain
    """

    def __init__(
        self,
        name=None,
        k=1.0,
        v1_ic=None,
        x1_ic=None,
        v2_ic=None,
        x2_ic=None,
    ):
        self.name = "mts" if name is None else name
        super().__init__(self.name, v1_ic=v1_ic, x1_ic=x1_ic, v2_ic=v2_ic, x2_ic=x2_ic)

        # maybe not a necessary contraint, but doing it for now to avoid confusing myself when debugging.
        if k <= 0.0:
            raise ValueError(
                f"Component {self.__class__.__name__ } {self.name} must have k>0"
            )

        self.k = sym(self.name + "_k", kind="param", val=k)
        self.syms.add(self.k)
        self.eqs.add(eqn(e=Eq(self.f1.s, self.k.s * (self.x1.s - self.x2.s))))


class MechTransDamper(MechTransTwoPort):
    """
    ideal damper in mechanical translational domain
    """

    def __init__(
        self,
        name=None,
        c=1.0,
        v1_ic=None,
        x1_ic=None,
        v2_ic=None,
        x2_ic=None,
    ):
        self.name = "mtd" if name is None else name
        super().__init__(self.name, v1_ic=v1_ic, x1_ic=x1_ic, v2_ic=v2_ic, x2_ic=x2_ic)

        # maybe not a necessary contraint, but doing it for now to avoid confusing myself when debugging.
        if c <= 0.0:
            raise ValueError(
                f"Component {self.__class__.__name__ } {self.name} must have c>0"
            )

        self.c = sym(self.name + "_c", kind="param", val=c)
        self.syms.add(self.c)
        self.eqs.add(eqn(e=Eq(self.f1.s, self.c.s * (self.v1.s - self.v2.s))))


class MechTransRef(MechTransOnePort):
    """
    rigid(non-moving) reference in mechanical translational domain
    """

    def __init__(self, name=None, x_ic=None):
        self.name = "mtr" if name is None else name
        super().__init__(self.name, v_ic=0, x_ic=x_ic)
        self.eqs = set([eqn(e=Eq(0, self.a.s)), eqn(e=Eq(0, self.v.s))])

        # this sucks. need this here because not all one port blocks
        # use the 'input' of the block.
        self.port_idx_to_name = {1: "p"}


class MechRotPort(PortBase):
    """
    port for a rotational mechanical component to interface with others.
    """

    def __init__(self, w_sym=None, t_sym=None):
        self.flow = t_sym
        self.pot = w_sym


class MechRotOnePort(ComponentBase):
    """
    a partial component with one mechanical rotational connection.
    """

    def __init__(self, name, w_ic=None, ang_ic=None, p="p"):
        print(f"MechRotOnePort __init__() for cpm:{name}")
        self.t = sym(name + "_t", kind="flow")
        self.alpha = sym(name + "_alpha", kind="var")
        self.w = sym(name + "_w", kind="pot", der_sym=self.alpha.s, ic=w_ic)
        self.ang = sym(name + "_ang", kind="var", der_sym=self.w.s, ic=ang_ic)

        self.ports = {p: MechRotPort(w_sym=self.w, t_sym=self.t)}

        self.syms = set([self.t, self.alpha, self.w, self.ang])

        self.port_idx_to_name = {-1: p}


class MechRotTwoPort(ComponentBase):
    """
    a partial component with two mechanical rotational connections.
    """

    def __init__(
        self, name, ang1_ic=None, w1_ic=None, ang2_ic=None, w2_ic=None, p1="p1", p2="p2"
    ):
        print(f"MechRotTwoPort __init__() for cpm:{name}")
        self.t1 = sym(self.name + "_t1", kind="flow")
        self.t2 = sym(self.name + "_t2", kind="flow")
        self.alpha1 = sym(self.name + "_alpha1", kind="var")
        self.w1 = sym(self.name + "_w1", kind="pot", der_sym=self.alpha1.s, ic=w1_ic)
        self.ang1 = sym(self.name + "_ang1", kind="var", der_sym=self.w1.s, ic=ang1_ic)
        self.alpha2 = sym(self.name + "_alpha2", kind="var")
        self.w2 = sym(self.name + "_w2", kind="pot", der_sym=self.alpha2.s, ic=w2_ic)
        self.ang2 = sym(self.name + "_ang2", kind="var", der_sym=self.w2.s, ic=ang2_ic)

        self.ports = {
            p1: MechRotPort(w_sym=self.w1, t_sym=self.t1),
            p2: MechRotPort(w_sym=self.w2, t_sym=self.t2),
        }
        self.syms = set(
            [
                self.t1,
                self.t2,
                self.alpha1,
                self.w1,
                self.ang1,
                self.alpha2,
                self.w2,
                self.ang2,
            ]
        )
        self.eqs = set([eqn(e=Eq(0, self.t1.s + self.t2.s))])

        self.port_idx_to_name = {-1: p1, 1: p2}


class MechRotTorque(MechRotOnePort):
    """
    ideal torque source in mechanical rotational domain
    """

    def __init__(self, name=None, torque=0.0):
        self.name = "mrt" if name is None else name
        super().__init__(self.name)
        self.tparam = sym(self.name + "_tparam", kind="param", val=torque)
        self.syms.add(self.tparam)
        self.eqs = set([eqn(e=Eq(self.tparam.s, self.t.s))])

        # this sucks. need this here because not all one port blocks
        # use the 'input' of the block.
        self.port_idx_to_name = {1: "p"}


class MechRotInertia(MechRotOnePort):
    """
    ideal inertia in mechanical rotational domain
    """

    def __init__(self, name=None, I=1.0, w_ic=None, ang_ic=None):  # noqa
        self.name = "mri" if name is None else name
        super().__init__(self.name, w_ic=w_ic, ang_ic=ang_ic)

        if I <= 0.0:
            raise ValueError(
                f"Component {self.__class__.__name__ } {self.name} must have I>0"
            )

        self.I = sym(self.name + "_I", kind="param", val=I)  # noqa
        self.syms.add(self.I)
        self.eqs = set([eqn(e=Eq(self.t.s, self.I.s * self.alpha.s))])


class MechRotSpring(MechRotTwoPort):
    """
    ideal spring in mechanical rotational domain
    """

    def __init__(
        self,
        name=None,
        k=1.0,
        w1_ic=None,
        ang1_ic=None,
        w2_ic=None,
        ang2_ic=None,
    ):
        self.name = "mrs" if name is None else name
        super().__init__(
            self.name, w1_ic=w1_ic, ang1_ic=ang1_ic, w2_ic=w2_ic, ang2_ic=ang2_ic
        )

        # maybe not a necessary contraint, but doing it for now to avoid confusing myself when debugging.
        if k <= 0.0:
            raise ValueError(
                f"Component {self.__class__.__name__ } {self.name} must have k>0"
            )

        self.k = sym(self.name + "_k", kind="param", val=k)
        self.syms.add(self.k)
        self.eqs.add(eqn(e=Eq(self.t1.s, self.k.s * (self.ang1.s - self.ang2.s))))


class MechRotDamper(MechRotTwoPort):
    """
    ideal damper in mechanical rotational domain
    """

    def __init__(
        self,
        name=None,
        c=1.0,
        w1_ic=None,
        ang1_ic=None,
        w2_ic=None,
        ang2_ic=None,
    ):
        self.name = "mtd" if name is None else name
        super().__init__(
            self.name, w1_ic=w1_ic, ang1_ic=ang1_ic, w2_ic=w2_ic, ang2_ic=ang2_ic
        )

        # maybe not a necessary contraint, but doing it for now to avoid confusing myself when debugging.
        if c <= 0.0:
            raise ValueError(
                f"Component {self.__class__.__name__ } {self.name} must have c>0"
            )

        self.c = sym(self.name + "_c", kind="param", val=c)
        self.syms.add(self.c)
        self.eqs.add(eqn(e=Eq(self.t1.s, self.c.s * (self.w1.s - self.w2.s))))


class MechRotRef(MechRotOnePort):
    """
    rigid(non-moving) reference in mechanical rotational domain
    """

    def __init__(self, name=None, x_ic=None):
        self.name = "mrr" if name is None else name
        super().__init__(self.name, w_ic=0, ang_ic=x_ic)
        self.eqs = set([eqn(e=Eq(0, self.alpha.s)), eqn(e=Eq(0, self.w.s))])

        # this sucks. need this here because not all one port blocks
        # use the 'input' of the block.
        self.port_idx_to_name = {1: "p"}


class CustomComponent(ComponentBase):
    """
    a user defined component.
    might be used if parsing modelica block code, and creating component.
    """

    def __init__(self, name=None):
        self.name = "cstm" if name is None else name
        self.syms_lookup = {}

    def add_sym(self, suffix="", val=None, der_sym=None, kind=None, expr=None, ic=None):
        self.syms.add(sym(name=self.name + suffix, val=val, der_sym=der_sym, kind=kind))
        # TODO: is there a way to add just this sym to the syms_lookup ?

    def lift_to_mech_one_port(self, x_ic=None, v_ic=None):
        MechTransOnePort.__init__(self, self.name, v_ic=v_ic, x_ic=x_ic)

    def lift_to_mech_two_port(self, x1_ic=None, v1_ic=None, x2_ic=None, v2_ic=None):
        MechTransTwoPort.__init__(
            self, self.name, v1_ic=v1_ic, x1_ic=x1_ic, v2_ic=v2_ic, x2_ic=x2_ic
        )

    # @am. i think we need to find a better way to do this
    # presently, for users of this class to 'add' equations which reference
    # symbols they added using add_sym(), then need to get a handle on the symbol
    # object first generating this lookup map, and then getting the handle from it.
    # this means thye need to know they have to call this before they can use add_equation()
    def gen_syms_lookup(self):
        self.syms_lookup = {}
        for sym_ in self.syms:
            self.syms_lookup[sym_.name] = sym_

    def add_equation(self, e, kind=None):
        self.eqs.add(eqn(e=e, kind=kind))
