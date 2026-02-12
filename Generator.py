class Generator:
    """
    Represents a generator connected to a bus
    with specified operating setpoints.
    """

    def __init__(self, name: str, bus1_name: str,
                 voltage_setpoint: float, mw_setpoint: float):

        self.name = name
        self.bus1_name = bus1_name
        self.voltage_setpoint = voltage_setpoint
        self.mw_setpoint = mw_setpoint

    def __repr__(self):
        return (f"Generator(name={self.name}, "
                f"bus={self.bus1_name}, "
                f"Vset={self.voltage_setpoint}, "
                f"MWset={self.mw_setpoint})")

