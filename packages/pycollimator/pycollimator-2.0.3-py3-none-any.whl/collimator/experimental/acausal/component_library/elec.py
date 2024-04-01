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

"""
Discussion on the design of the electrical components relative to Modelica Standard Library (MLS).

MSL Pin.mo defines the I(flow), and V. We do the similar in ElecPort, but the symbols are passed in from
the component, so we get I1, I2, V1, V2.

MSL TwoPin.mo and OnePort.mo define the component I and V symbols. We do similar, but define V in Elec2Pin,
and use the I1 from component for I.

In this way, the ElecResistor and ElecCapacitor end up with essetially an analogous set of symbols, and
an equivalent set of equations relative to the MSL components.
"""


class ElecPort(PortBase):
    """
    port for a electrical component to interface with others.
    """

    def __init__(self, name=None, V_sym=None, I_sym=None):
        self.name = name
        self.pot = V_sym
        self.flow = I_sym


class Elec2Pin(ComponentBase):
    """
    electrical domain component with 2 pins.
    Incomplete component.
    """

    def __init__(self, name, v_der_sym=None, V_ic=None, p1="plus", p2="minus"):
        self.V = sym(name + "_V", kind="var", der_sym=v_der_sym, ic=V_ic)
        self.V1 = sym(name + "_V1", kind="pot")
        self.V2 = sym(name + "_V2", kind="pot")
        self.I1 = sym(name + "_I1", kind="flow")
        self.I2 = sym(name + "_I2", kind="flow")

        self.ports = {
            p1: ElecPort(name=p1, V_sym=self.V1, I_sym=self.I1),
            p2: ElecPort(name=p2, V_sym=self.V2, I_sym=self.I2),
        }

        self.syms = set([self.V, self.V1, self.V2, self.I1, self.I2])
        self.eqs = set(
            [
                eqn(e=Eq(self.V1.s - self.V2.s, self.V.s)),
                eqn(e=Eq(0, self.I1.s + self.I2.s)),
            ]
        )

        self.port_idx_to_name = {-1: p1, 1: p2}


class ElecVoltageSource(Elec2Pin):
    """
    ideal constant voltage source in electrical domain
    """

    def __init__(self, name=None, voltage=1.0):
        self.name = "ecv" if name is None else name
        super().__init__(self.name)

        self.Vparam = sym(self.name + "_Vparam", kind="param", val=voltage)
        self.syms.add(self.Vparam)
        self.eqs.add(eqn(e=Eq(self.V.s, self.Vparam.s)))


class ElecVoltageSourceControlled(Elec2Pin):
    """
    ideal controlled voltage source in electrical domain
    """

    def __init__(self, name=None):
        self.name = "ecvc" if name is None else name
        super().__init__(self.name)

        self.Vin = sym(self.name + "_Vin", kind="in")
        self.syms.add(self.Vin)
        self.eqs.add(eqn(e=Eq(self.V.s, self.Vin.s)))


class ElecRef(ComponentBase):
    """
    *ground* reference in electrical domain
    """

    def __init__(self, name=None):
        self.name = "er" if name is None else name

        self.I = sym(self.name + "_I", kind="flow")  # noqa
        self.dV = sym(self.name + "_dV", kind="var")
        self.V = sym(self.name + "_V", kind="pot", der_sym=self.dV.s)

        self.ports = {"minus": ElecPort(V_sym=self.V, I_sym=self.I)}
        self.syms = set([self.I, self.dV, self.V])
        self.eqs = set(
            [eqn(e=Eq(0, self.dV.s)), eqn(e=Eq(0, self.V.s)), eqn(e=Eq(0, self.I.s))]
        )

        self.port_idx_to_name = {-1: "minus"}


class ElecResistor(Elec2Pin):
    """
    ideal resistor in electrical domain
    """

    def __init__(self, name=None, R=1.0):
        self.name = "er" if name is None else name
        super().__init__(self.name)

        if R <= 0.0:
            raise ValueError(f"Component ElecResistor {self.name} must have R>0")

        self.R = sym(self.name + "_R", kind="param", val=R)
        self.syms.add(self.R)
        self.eqs.add(eqn(e=Eq(self.V.s, self.I1.s * self.R.s)))


class ElecCapacitor(Elec2Pin):
    """
    ideal capacitor in electrical domain
    """

    def __init__(self, name=None, C=1.0, V_ic=0.0):
        self.name = "ec" if name is None else name

        if C <= 0.0:
            raise ValueError(f"Component ElecCapacitor {self.name} must have C>0")

        self.dV = sym(self.name + "_dV", kind="var")
        super().__init__(self.name, v_der_sym=self.dV.s, V_ic=V_ic)
        self.C = sym(self.name + "_C", kind="param", val=C)
        self.syms.update(set([self.C, self.dV]))
        self.eqs.add(eqn(e=Eq(self.I1.s, self.C.s * self.dV.s)))


class ElecVoltageSensor(ComponentBase):
    """
    ideal voltage sensor in electrical domain
    """

    def __init__(self, name=None, p1="plus", p2="minus"):
        self.name = "evs" if name is None else name
        self.Vout = sym(self.name + "_Vout", kind="out")
        self.V1 = sym(self.name + "_V1", kind="pot")
        self.V2 = sym(self.name + "_V2", kind="pot")

        self.ports = {
            p1: ElecPort(V_sym=self.V1),
            p2: ElecPort(V_sym=self.V2),
        }

        self.syms = set([self.Vout, self.V1, self.V2])
        self.eqs = set(
            [
                eqn(e=Eq(self.V1.s - self.V2.s, self.Vout.s)),
            ]
        )

        # although the UI shows this block with 2 ports on the left side
        # here the causal port (the voltage input) is defined using the
        # Vout variable and its corresponding equation. So this map only
        # needs toie two acaual ports.
        self.port_idx_to_name = {-1: p1, 1: p2}


class ElecCurrentSensor(ComponentBase):
    """
    ideal current sensor in electrical domain
    """

    # FIXME: this may need potential variables V1 and V2.

    def __init__(self, name=None, p1="plus", p2="minus"):
        self.name = "evs" if name is None else name
        self.Iout = sym(self.name + "_Iout", kind="out")
        self.I1 = sym(self.name + "_I1", kind="pot")
        self.I2 = sym(self.name + "_I2", kind="pot")

        self.ports = {
            p1: ElecPort(I_sym=self.I1),
            p2: ElecPort(I_sym=self.I2),
        }

        self.syms = set([self.Iout, self.I1, self.I2])
        self.eqs = set(
            [
                eqn(e=Eq(0, self.I1.s - self.I2.s)),
                eqn(e=Eq(self.I1.s, self.Iout.s)),
            ]
        )

        # although the UI shows this block with 2 ports on the left side
        # here the causal port (the voltage input) is defined using the
        # Vout variable and its corresponding equation. So this map only
        # needs toie two acaual ports.
        self.port_idx_to_name = {-1: p1, 1: p2}


# class ElecMotor(MechRotOnePort, Elec2Pin):
class ElecMotor:
    """
    ideal DC electric motor
    """

    # FIXME how do properly inherit from 2 classes?

    def __init__(self, name=None, Kt=1.0, Kv=1e-3, R=0.1):
        self.name = "motor" if name is None else name
        # MechRotOnePort.__init__(self, self.name, p="pm")
        # print(f"self.ports={self.ports}")
        # Elec2Pin.__init__(self, self.name, p1="pe1", p2="pe2")
        # # super(ElecMotor, self).__init__()
        # print(f"self.ports={self.ports}")
        # print(f"self.syms={self.syms}")
        # print(f"self.eqs={self.eqs}")

        # self.Kt = sym(name + "_Kt", kind="param", val=Kt)
        # self.Kv = sym(name + "_Kv", kind="param", val=Kv)
        # self.R = sym(name + "_R", kind="param", val=R)

        # self.t = sym(name + "_t", kind="flow")
        # self.alpha = sym(name + "_alpha", kind="var")
        # self.w = sym(name + "_w", kind="pot", der_sym=self.alpha.s, ic=0)
        # self.ang = sym(name + "_ang", kind="var", der_sym=self.w.s, ic=0)

        # self.ports["pm"] = MechRotPort(w_sym=self.w, t_sym=self.t)

        # self.syms.update(
        #     [self.t, self.alpha, self.w, self.ang, self.Kt, self.Kv, self.R]
        # )

        # print(f"\nself.ports={self.ports}")
        # print(f"self.syms={self.syms}")
        # print(f"self.eqs={self.eqs}")

        # # toqrue = Kt*current
        # self.eqs.add(eqn(e=Eq(self.t.s, self.Kt.s * self.I1.s)))
        # # backEMF = v1-v2 = Kv*speed
        # self.eqs.add(
        #     eqn(
        #         e=Eq(
        #             (self.V1.s - self.V2.s) - (self.Kv.s * self.w.s),
        #             self.I1.s * self.R.s,
        #         )
        #     )
        # )

        # print(f"self.eqs={self.eqs}")
