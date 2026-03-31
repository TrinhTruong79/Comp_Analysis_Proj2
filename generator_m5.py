# generator_m5.py
# Milestone 5: Refactored Generator class with per-unit real power injection


class GeneratorM5:
    """
    Milestone 5 Generator:
    - Keeps Milestone 1 parameters: name, bus1_name, voltage_setpoint, mw_setpoint
    - Adds:
        p       : Per-unit real power injection
        calc_p(): Returns per-unit real power injection
    """

    def __init__(self, name, bus1_name, voltage_setpoint, mw_setpoint, p=0.0):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Generator name must be a non-empty string.")
        if not isinstance(bus1_name, str) or not bus1_name.strip():
            raise ValueError("Generator bus1_name must be a non-empty string.")
        if float(voltage_setpoint) <= 0:
            raise ValueError("Generator voltage_setpoint must be > 0.")

        self.name = name
        self.bus1_name = bus1_name
        self.voltage_setpoint = float(voltage_setpoint)
        self.mw_setpoint = float(mw_setpoint)
        self.p = float(p)

    def calc_p(self):
        """Return per-unit real power injection."""
        return self.p
