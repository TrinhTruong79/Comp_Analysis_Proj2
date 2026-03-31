# bus_m5.py
# Milestone 5: Refactored Bus class with voltage state variables and bus type


class BusM5:
    """
    Milestone 5 Bus:
    - Keeps Milestone 1 parameters: name, nominal_kv, bus_index
    - Adds:
        vpu       : Per-unit voltage magnitude (default 1.0)
        delta     : Voltage phase angle in degrees (default 0.0)
        bus_type  : 'Slack', 'PQ', or 'PV'
    """

    VALID_BUS_TYPES = {"Slack", "PQ", "PV"}
    _counter = 0

    def __init__(self, name, nominal_kv, bus_type="PQ", vpu=1.0, delta=0.0):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Bus name must be a non-empty string.")
        if float(nominal_kv) <= 0:
            raise ValueError("Bus nominal_kv must be > 0.")
        if bus_type not in self.VALID_BUS_TYPES:
            raise ValueError(
                f"Invalid bus_type '{bus_type}'. "
                f"Allowed types: {self.VALID_BUS_TYPES}"
            )

        self.name = name
        self.nominal_kv = float(nominal_kv)
        self.bus_type = bus_type
        self.vpu = float(vpu)
        self.delta = float(delta)

        self.bus_index = BusM5._counter
        BusM5._counter += 1

    @classmethod
    def reset_counter(cls):
        cls._counter = 0
