# circuit_m7.py
# Unified Circuit class covering Milestones 4 through 7
#   - Milestone 4: Ybus construction
#   - Milestone 5: Settings integration, refactored bus/gen/load
#   - Milestone 6: Power injection equations, mismatch vector
#   - Milestone 7: Jacobian matrix construction

import numpy as np
import pandas as pd

from bus_m5 import BusM5
from generator_m5 import GeneratorM5
from load_m5 import LoadM5
from transformer_m3 import TransformerM3
from transmission_line_m3 import TransmissionLineM3
from settings import Settings


class CircuitM7:
    """
    Full Circuit class for power flow analysis (Milestones 4-7).

    Stores all equipment and provides methods for:
      - Ybus construction          (Milestone 4)
      - Power injection            (Milestone 6)
      - Power mismatch             (Milestone 6)
      - Jacobian matrix            (Milestone 7)
    """

    def __init__(self, name, settings=None):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Circuit name must be a non-empty string.")

        self.name = name
        self.settings = settings if settings is not None else Settings()

        self.buses = {}
        self.transformers = {}
        self.transmission_lines = {}
        self.generators = {}
        self.loads = {}

        self.ybus = None

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------
    @staticmethod
    def _ensure_unique(store, component_name, equipment_type):
        if component_name in store:
            raise ValueError(
                f"Duplicate {equipment_type} name '{component_name}'. "
                f"Each {equipment_type} name must be unique."
            )

    # ------------------------------------------------------------------
    # Add methods (using M5 classes for Bus, Generator, Load)
    # ------------------------------------------------------------------
    def add_bus(self, name, nominal_kv, bus_type="PQ", vpu=1.0, delta=0.0):
        self._ensure_unique(self.buses, name, "bus")
        obj = BusM5(name, nominal_kv, bus_type, vpu, delta)
        self.buses[name] = obj
        return obj

    def add_transformer(self, name, bus1_name, bus2_name, r, x):
        self._ensure_unique(self.transformers, name, "transformer")
        obj = TransformerM3(name, bus1_name, bus2_name, r, x)
        self.transformers[name] = obj
        return obj

    def add_transmission_line(self, name, bus1_name, bus2_name, r, x, g, b):
        self._ensure_unique(self.transmission_lines, name, "transmission line")
        obj = TransmissionLineM3(name, bus1_name, bus2_name, r, x, g, b)
        self.transmission_lines[name] = obj
        return obj

    def add_generator(self, name, bus1_name, voltage_setpoint, mw_setpoint, p=0.0):
        self._ensure_unique(self.generators, name, "generator")
        obj = GeneratorM5(name, bus1_name, voltage_setpoint, mw_setpoint, p)
        self.generators[name] = obj
        return obj

    def add_load(self, name, bus1_name, mw, mvar, p=0.0, q=0.0):
        self._ensure_unique(self.loads, name, "load")
        obj = LoadM5(name, bus1_name, mw, mvar, p, q)
        self.loads[name] = obj
        return obj

    # ==================================================================
    # MILESTONE 4 — Ybus
    # ==================================================================
    def calc_ybus(self):
        """Build the N×N Ybus admittance matrix and store in self.ybus."""
        bus_names = list(self.buses.keys())
        n = len(bus_names)
        if n == 0:
            raise ValueError("Cannot build Ybus: circuit has no buses.")

        bus_to_idx = {bn: i for i, bn in enumerate(bus_names)}
        Y = np.zeros((n, n), dtype=complex)

        def stamp(yprim, b1, b2):
            if b1 not in bus_to_idx or b2 not in bus_to_idx:
                raise ValueError(
                    f"Element connects to '{b1}' and '{b2}', "
                    f"but one or both buses are missing."
                )
            i, j = bus_to_idx[b1], bus_to_idx[b2]
            Y[i, i] += yprim.loc[b1, b1]
            Y[i, j] += yprim.loc[b1, b2]
            Y[j, i] += yprim.loc[b2, b1]
            Y[j, j] += yprim.loc[b2, b2]

        for t in self.transformers.values():
            stamp(t.calc_yprim(), t.bus1_name, t.bus2_name)
        for line in self.transmission_lines.values():
            stamp(line.calc_yprim(), line.bus1_name, line.bus2_name)

        self.ybus = pd.DataFrame(Y, index=bus_names, columns=bus_names)

    # ==================================================================
    # MILESTONE 6 — Power Injection & Mismatch
    # ==================================================================
    def compute_power_injection(self, bus_name, ybus_np, bus_names, voltages, angles):
        """
        Compute real and reactive power injection at a given bus.

        Parameters
        ----------
        bus_name : str
        ybus_np  : 2-D numpy complex array (N×N)
        bus_names: list of str (ordered same as ybus rows/cols)
        voltages : 1-D numpy array of |V| for each bus (p.u.)
        angles   : 1-D numpy array of delta for each bus (radians)

        Returns
        -------
        (Pi, Qi) : tuple of floats
        """
        idx = bus_names.index(bus_name)
        Vi = voltages[idx]
        n = len(bus_names)

        Pi = 0.0
        Qi = 0.0
        for j in range(n):
            Vj = voltages[j]
            Yij = ybus_np[idx, j]
            Gij = Yij.real
            Bij = Yij.imag
            delta_ij = angles[idx] - angles[j]

            Pi += Vj * (Gij * np.cos(delta_ij) + Bij * np.sin(delta_ij))
            Qi += Vj * (Gij * np.sin(delta_ij) - Bij * np.cos(delta_ij))

        Pi *= Vi
        Qi *= Vi
        return Pi, Qi

    def _get_bus_specified_power(self, bus_name):
        """
        Sum the scheduled / specified P and Q injections at a bus.

        Convention:
          generators inject positive P
          loads consume (negative injection)

        Returns
        -------
        (Pspec, Qspec) in per-unit
        """
        Pspec = 0.0
        Qspec = 0.0

        for gen in self.generators.values():
            if gen.bus1_name == bus_name:
                Pspec += gen.calc_p()

        for load in self.loads.values():
            if load.bus1_name == bus_name:
                Pspec -= load.calc_p()
                Qspec -= load.calc_q()

        return Pspec, Qspec

    def compute_power_mismatch(self, voltages, angles):
        """
        Compute the power mismatch vector f = [ΔP₂…ΔPₙ, ΔQ_pq…]

        Ordering:
          - ΔP for every non-slack bus (in bus-order)
          - ΔQ for every PQ bus (in bus-order)

        Parameters
        ----------
        voltages : 1-D array, |V| per bus (ordered by self.buses keys)
        angles   : 1-D array, δ per bus in radians

        Returns
        -------
        mismatch : 1-D numpy array
        """
        if self.ybus is None:
            raise ValueError("Ybus has not been computed. Call calc_ybus() first.")

        bus_names = list(self.buses.keys())
        ybus_np = self.ybus.values

        delta_p_list = []
        delta_q_list = []

        for bname in bus_names:
            bus = self.buses[bname]
            if bus.bus_type == "Slack":
                continue

            Pcalc, Qcalc = self.compute_power_injection(
                bname, ybus_np, bus_names, voltages, angles
            )
            Pspec, Qspec = self._get_bus_specified_power(bname)

            delta_p_list.append(Pspec - Pcalc)

            if bus.bus_type == "PQ":
                delta_q_list.append(Qspec - Qcalc)

        mismatch = np.array(delta_p_list + delta_q_list)
        return mismatch

    # ==================================================================
    # MILESTONE 7 — Jacobian Matrix
    # ==================================================================
    def calc_jacobian(self, voltages, angles):
        """
        Build the Jacobian matrix partitioned as:

            J = | J1  J2 |
                | J3  J4 |

        where:
            J1 = ∂P/∂δ     (non-slack buses × non-slack buses)
            J2 = ∂P/∂|V|   (non-slack buses × PQ buses)
            J3 = ∂Q/∂δ     (PQ buses × non-slack buses)
            J4 = ∂Q/∂|V|   (PQ buses × PQ buses)

        Parameters
        ----------
        voltages : 1-D array, |V| per bus
        angles   : 1-D array, δ per bus in radians

        Returns
        -------
        J : 2-D numpy array  (2N-2-Npv) × (2N-2-Npv)
        """
        if self.ybus is None:
            raise ValueError("Ybus has not been computed. Call calc_ybus() first.")

        bus_names = list(self.buses.keys())
        ybus_np = self.ybus.values
        n = len(bus_names)

        # Identify index lists
        non_slack_indices = []  # indices into bus_names for non-slack buses
        pq_indices = []         # indices into bus_names for PQ buses

        for k, bname in enumerate(bus_names):
            bt = self.buses[bname].bus_type
            if bt != "Slack":
                non_slack_indices.append(k)
            if bt == "PQ":
                pq_indices.append(k)

        n_ns = len(non_slack_indices)   # number of non-slack buses
        n_pq = len(pq_indices)          # number of PQ buses

        J1 = np.zeros((n_ns, n_ns))
        J2 = np.zeros((n_ns, n_pq))
        J3 = np.zeros((n_pq, n_ns))
        J4 = np.zeros((n_pq, n_pq))

        # Pre-compute P_calc and Q_calc for each bus (useful for diagonal terms)
        P_calc = np.zeros(n)
        Q_calc = np.zeros(n)
        for i in range(n):
            Vi = voltages[i]
            for j in range(n):
                Vj = voltages[j]
                Yij = ybus_np[i, j]
                Gij = Yij.real
                Bij = Yij.imag
                dij = angles[i] - angles[j]
                P_calc[i] += Vi * Vj * (Gij * np.cos(dij) + Bij * np.sin(dij))
                Q_calc[i] += Vi * Vj * (Gij * np.sin(dij) - Bij * np.cos(dij))

        # ------- J1: ∂P_i / ∂δ_j  (non-slack × non-slack) -------
        for r_idx, i in enumerate(non_slack_indices):
            Vi = voltages[i]
            for c_idx, j in enumerate(non_slack_indices):
                Vj = voltages[j]
                Yij = ybus_np[i, j]
                Gij = Yij.real
                Bij = Yij.imag
                dij = angles[i] - angles[j]

                if i == j:
                    # ∂Pi/∂δi = -Qi - Bii * Vi^2
                    Bii = ybus_np[i, i].imag
                    J1[r_idx, c_idx] = -Q_calc[i] - Bii * Vi**2
                else:
                    # ∂Pi/∂δj = Vi * Vj * (Gij*sin(δij) - Bij*cos(δij))
                    J1[r_idx, c_idx] = Vi * Vj * (Gij * np.sin(dij) - Bij * np.cos(dij))

        # ------- J2: ∂P_i / ∂|V_j|  (non-slack × PQ) -------
        for r_idx, i in enumerate(non_slack_indices):
            Vi = voltages[i]
            for c_idx, j in enumerate(pq_indices):
                Vj = voltages[j]
                Yij = ybus_np[i, j]
                Gij = Yij.real
                Bij = Yij.imag
                dij = angles[i] - angles[j]

                if i == j:
                    # ∂Pi/∂|Vi| = Pi/|Vi| + Gii*|Vi|
                    Gii = ybus_np[i, i].real
                    J2[r_idx, c_idx] = P_calc[i] / Vi + Gii * Vi
                else:
                    # ∂Pi/∂|Vj| = Vi * (Gij*cos(δij) + Bij*sin(δij))
                    J2[r_idx, c_idx] = Vi * (Gij * np.cos(dij) + Bij * np.sin(dij))

        # ------- J3: ∂Q_i / ∂δ_j  (PQ × non-slack) -------
        for r_idx, i in enumerate(pq_indices):
            Vi = voltages[i]
            for c_idx, j in enumerate(non_slack_indices):
                Vj = voltages[j]
                Yij = ybus_np[i, j]
                Gij = Yij.real
                Bij = Yij.imag
                dij = angles[i] - angles[j]

                if i == j:
                    # ∂Qi/∂δi = Pi - Gii * Vi^2
                    Gii = ybus_np[i, i].real
                    J3[r_idx, c_idx] = P_calc[i] - Gii * Vi**2
                else:
                    # ∂Qi/∂δj = -Vi * Vj * (Gij*cos(δij) + Bij*sin(δij))
                    J3[r_idx, c_idx] = -Vi * Vj * (Gij * np.cos(dij) + Bij * np.sin(dij))

        # ------- J4: ∂Q_i / ∂|V_j|  (PQ × PQ) -------
        for r_idx, i in enumerate(pq_indices):
            Vi = voltages[i]
            for c_idx, j in enumerate(pq_indices):
                Vj = voltages[j]
                Yij = ybus_np[i, j]
                Gij = Yij.real
                Bij = Yij.imag
                dij = angles[i] - angles[j]

                if i == j:
                    # ∂Qi/∂|Vi| = Qi/|Vi| - Bii*|Vi|
                    Bii = ybus_np[i, i].imag
                    J4[r_idx, c_idx] = Q_calc[i] / Vi - Bii * Vi
                else:
                    # ∂Qi/∂|Vj| = Vi * (Gij*sin(δij) - Bij*cos(δij))
                    J4[r_idx, c_idx] = Vi * (Gij * np.sin(dij) - Bij * np.cos(dij))

        # Assemble full Jacobian
        J_top = np.hstack([J1, J2])
        J_bot = np.hstack([J3, J4])
        J = np.vstack([J_top, J_bot])

        return J
