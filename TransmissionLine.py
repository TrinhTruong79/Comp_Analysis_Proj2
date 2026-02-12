class TransmissionLine:
    """
    Represents a transmission line connecting two buses
    using lumped parameters.
    """

    def __init__(self, name: str, bus1_name: str, bus2_name: str,
                 r: float, x: float, g: float, b: float):
        """
        Initialize a TransmissionLine object.

        Parameters
        ----------
        name : str
        bus1_name : str
        bus2_name : str
        r : float
            Series resistance
        x : float
            Series reactance
        g : float
            Shunt conductance
        b : float
            Shunt susceptance
        """

        self.name = name
        self.bus1_name = bus1_name
        self.bus2_name = bus2_name
        self.r = r
        self.x = x
        self.g = g
        self.b = b

    def __repr__(self):
        return (f"TransmissionLine(name={self.name}, "
                f"bus1={self.bus1_name}, bus2={self.bus2_name}, "
                f"r={self.r}, x={self.x}, g={self.g}, b={self.b})")

