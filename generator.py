# generator.py

class Generator:
    """
    Represents a generator connected to a bus.

    Required:
      - name (str)
      - bus1_name (str)
      - voltage_setpoint (float)
      - mw_setpoint (float)
    """

    def __init__(self, name, bus1_name, voltage_setpoint, mw_setpoint):
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