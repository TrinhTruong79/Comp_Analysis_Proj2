# load.py

class Load:
    """
    Represents a load connected to a bus.

    Required:
      - name (str)
      - bus1_name (str)
      - mw (float)
      - mvar (float)
    """

    def __init__(self, name, bus1_name, mw, mvar):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Load name must be a non-empty string.")
        if not isinstance(bus1_name, str) or not bus1_name.strip():
            raise ValueError("Load bus1_name must be a non-empty string.")

        self.name = name
        self.bus1_name = bus1_name
        self.mw = float(mw)
        self.mvar = float(mvar)