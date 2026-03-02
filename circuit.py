# circuit.py
from bus import Bus
from transformer import Transformer
from transmission_line import TransmissionLine
from generator import Generator
from load import Load


class Circuit:
    """
    Circuit class stores all equipment in dictionaries.

    Required attributes :
      - buses
      - transformers
      - transmission_lines
      - generators
      - loads
    """

    def __init__(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Circuit name must be a non empty string.")

        self.name = name
        self.buses = {}
        self.transformers = {}
        self.transmission_lines = {}
        self.generators = {}
        self.loads = {}

    @staticmethod
    def _ensure_unique(store, component_name, equipment_type):
        if component_name in store:
            raise ValueError(
                f"Duplicate {equipment_type} name '{component_name}'. "
                f"Each {equipment_type} name must be unique."
            )

    def add_bus(self, name, nominal_kv):
        self._ensure_unique(self.buses, name, "bus")
        obj = Bus(name, nominal_kv)
        self.buses[name] = obj
        return obj

    def add_transformer(self, name, bus1_name, bus2_name, r, x):
        self._ensure_unique(self.transformers, name, "transformer")
        obj = Transformer(name, bus1_name, bus2_name, r, x)
        self.transformers[name] = obj
        return obj

    def add_transmission_line(self, name, bus1_name, bus2_name, r, x, g, b):
        self._ensure_unique(self.transmission_lines, name, "transmission line")
        obj = TransmissionLine(name, bus1_name, bus2_name, r, x, g, b)
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