class Bus:
    """
    Represents a bus (node) in a power system.
    """

    # Class-level counter to assign unique bus_index
    _bus_counter = 0

    def __init__(self, name: str, nominal_kv: float):
        """
        Initialize a Bus object.

        Parameters:
        -----------
        name : str
            Name of the bus.
        nominal_kv : float
            Nominal voltage level in kV.
        """

        self.name = name
        self.nominal_kv = nominal_kv

        # Assign unique bus index
        self.bus_index = Bus._bus_counter
        Bus._bus_counter += 1

    def __repr__(self):
        return f"Bus(name={self.name}, nominal_kv={self.nominal_kv}, bus_index={self.bus_index})"

