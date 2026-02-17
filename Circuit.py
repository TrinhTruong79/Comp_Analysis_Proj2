from Bus import Bus
from Transformer import Transformer
from TransmissionLine import TransmissionLine
from Generator import Generator
from Load import Load


class Circuit:
    """
    Circuit = container for a complete power system network.

    Stores equipment in dictionaries:
      - buses
      - transformers
      - transmission_lines
      - generators
      - loads

    Keys are component names (str), values are the corresponding objects.
    """

    def __init__(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Circuit name must be a non-empty string.")

        self.name = name.strip()

        # Required attributes (all dicts)
        self.buses = {}
        self.transformers = {}
        self.transmission_lines = {}
        self.generators = {}
        self.loads = {}

    # -------------------------
    # Internal helper
    # -------------------------
    @staticmethod
    def _check_duplicate(component_dict: dict, component_name: str, component_type: str) -> None:
        if component_name in component_dict:
            raise ValueError(
                f"Duplicate {component_type} name '{component_name}' detected. "
                f"Each {component_type} name must be unique."
            )

    # -------------------------
    # Add methods (Milestone 2)
    # -------------------------
    def add_bus(self, name: str, nominal_kv: float) -> Bus:
        """Create a Bus and store it in self.buses."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Bus name must be a non-empty string.")
        name = name.strip()

        self._check_duplicate(self.buses, name, "bus")

        bus = Bus(name, nominal_kv)
        self.buses[name] = bus
        return bus

    def add_transformer(self, name: str, bus1_name: str, bus2_name: str, r: float, x: float) -> Transformer:
        """Create a Transformer and store it in self.transformers."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Transformer name must be a non-empty string.")
        name = name.strip()

        self._check_duplicate(self.transformers, name, "transformer")

        # Per milestone: store bus references using bus names (strings)
        tr = Transformer(name, bus1_name, bus2_name, r, x)
        self.transformers[name] = tr
        return tr

    def add_transmission_line(
        self,
        name: str,
        bus1_name: str,
        bus2_name: str,
        r: float,
        x: float,
        g: float,
        b: float,
    ) -> TransmissionLine:
        """Create a TransmissionLine and store it in self.transmission_lines."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Transmission line name must be a non-empty string.")
        name = name.strip()

        self._check_duplicate(self.transmission_lines, name, "transmission line")

        line = TransmissionLine(name, bus1_name, bus2_name, r, x, g, b)
        self.transmission_lines[name] = line
        return line

    def add_generator(self, name: str, bus1_name: str, voltage_setpoint: float, mw_setpoint: float) -> Generator:
        """Create a Generator and store it in self.generators."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Generator name must be a non-empty string.")
        name = name.strip()

        self._check_duplicate(self.generators, name, "generator")

        gen = Generator(name, bus1_name, voltage_setpoint, mw_setpoint)
        self.generators[name] = gen
        return gen

    def add_load(self, name: str, bus1_name: str, mw: float, mvar: float) -> Load:
        """Create a Load and store it in self.loads."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Load name must be a non-empty string.")
        name = name.strip()

        self._check_duplicate(self.loads, name, "load")

        load = Load(name, bus1_name, mw, mvar)
        self.loads[name] = load
        return load

    def __repr__(self) -> str:
        return (
            f"Circuit(name={self.name!r}, "
            f"buses={len(self.buses)}, transformers={len(self.transformers)}, "
            f"transmission_lines={len(self.transmission_lines)}, "
            f"generators={len(self.generators)}, loads={len(self.loads)})"
        )