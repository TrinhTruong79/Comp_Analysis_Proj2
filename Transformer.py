class Transformer:
    """
    Represents a transformer connecting two buses.

    In this milestone, the transformer is modeled
    using its series impedance (r + jx).
    """

    def __init__(self, name: str, bus1_name: str, bus2_name: str,
                 r: float, x: float):
        """
        Initialize a Transformer object.

        Parameters
        ----------
        name : str
            Name of the transformer.
        bus1_name : str
            Name of the first bus.
        bus2_name : str
            Name of the second bus.
        r : float
            Series resistance (pu or ohm depending on convention).
        x : float
            Series reactance.
        """

        self.name = name
        self.bus1_name = bus1_name
        self.bus2_name = bus2_name
        self.r = r
        self.x = x

    def __repr__(self):
        return (f"Transformer(name={self.name}, "
                f"bus1={self.bus1_name}, "
                f"bus2={self.bus2_name}, "
                f"r={self.r}, x={self.x})")



