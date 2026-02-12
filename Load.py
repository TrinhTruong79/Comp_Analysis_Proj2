class Load:
    """
    Represents a constant real and reactive power load
    connected to a bus.
    """

    def __init__(self, name: str, bus1_name: str,
                 mw: float, mvar: float):

        self.name = name
        self.bus1_name = bus1_name
        self.mw = mw
        self.mvar = mvar

    def __repr__(self):
        return (f"Load(name={self.name}, "
                f"bus={self.bus1_name}, "
                f"MW={self.mw}, MVAR={self.mvar})")

