# transmission_line.py

class TransmissionLine:
    """
    Represents a transmission line connecting two buses.

    Required:
      - name (str)
      - bus1_name (str)
      - bus2_name (str)
      - r (float)
      - x (float)
      - g (float)
      - b (float)
    """

    def __init__(self, name, bus1_name, bus2_name, r, x, g, b):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("TransmissionLine name must be a non-empty string.")
        if not isinstance(bus1_name, str) or not bus1_name.strip():
            raise ValueError("TransmissionLine bus1_name must be a non-empty string.")
        if not isinstance(bus2_name, str) or not bus2_name.strip():
            raise ValueError("TransmissionLine bus2_name must be a non-empty string.")

        self.name = name
        self.bus1_name = bus1_name
        self.bus2_name = bus2_name
        self.r = float(r)
        self.x = float(x)
        self.g = float(g)
        self.b = float(b)