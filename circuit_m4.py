# circuit_m4.py
import numpy as np
import pandas as pd

from bus import Bus
from generator import Generator
from load import Load

from transformer_m3 import TransformerM3
from transmission_line_m3 import TransmissionLineM3


class CircuitM4:
    """
    Milestone 4 Circuit:
    - Same idea as Milestone 2: stores equipment in dicts
    - Adds:
        ybus attribute
        calc_ybus(): stamps Yprim matrices from transformers + lines into Ybus
    """

    def __init__(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Circuit name must be a non-empty string.")

        self.name = name

        self.buses = {}
        self.transformers = {}
        self.transmission_lines = {}
        self.generators = {}
        self.loads = {}

        self.ybus = None

    @staticmethod
    def _ensure_unique(store, component_name, equipment_type):
        if component_name in store:
            raise ValueError(
                f"Duplicate {equipment_type} name '{component_name}'. "
                f"Each {equipment_type} name must be unique."
            )

    # ---- Add methods ----
    def add_bus(self, name, nominal_kv):
        self._ensure_unique(self.buses, name, "bus")
        obj = Bus(name, nominal_kv)
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

    def add_generator(self, name, bus1_name, voltage_setpoint, mw_setpoint):
        self._ensure_unique(self.generators, name, "generator")
        obj = Generator(name, bus1_name, voltage_setpoint, mw_setpoint)
        self.generators[name] = obj
        return obj

    def add_load(self, name, bus1_name, mw, mvar):
        self._ensure_unique(self.loads, name, "load")
        obj = Load(name, bus1_name, mw, mvar)
        self.loads[name] = obj
        return obj

    # ---- Ybus build ----
    def calc_ybus(self):
        bus_names = list(self.buses.keys())
        n = len(bus_names)
        if n == 0:
            raise ValueError("Cannot build Ybus: circuit has no buses.")

        bus_to_idx = {bn: i for i, bn in enumerate(bus_names)}
        Y = np.zeros((n, n), dtype=complex)

        def stamp_2bus_yprim(yprim, b1, b2):
            if b1 not in bus_to_idx or b2 not in bus_to_idx:
                raise ValueError(
                    f"Element connects to '{b1}' and '{b2}', but one or both buses are missing."
                )

            i = bus_to_idx[b1]
            j = bus_to_idx[b2]

            Y[i, i] += yprim.loc[b1, b1]
            Y[i, j] += yprim.loc[b1, b2]
            Y[j, i] += yprim.loc[b2, b1]
            Y[j, j] += yprim.loc[b2, b2]

        for t in self.transformers.values():
            stamp_2bus_yprim(t.calc_yprim(), t.bus1_name, t.bus2_name)

        for line in self.transmission_lines.values():
            stamp_2bus_yprim(line.calc_yprim(), line.bus1_name, line.bus2_name)

        self.ybus = pd.DataFrame(Y, index=bus_names, columns=bus_names)