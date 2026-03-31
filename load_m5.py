# load_m5.py
# Milestone 5: Refactored Load class with per-unit real and reactive power


class LoadM5:
    """
    Milestone 5 Load:
    - Keeps Milestone 1 parameters: name, bus1_name, mw, mvar
    - Adds:
        p       : Per-unit real power consumption
        q       : Per-unit reactive power consumption
        calc_p(): Returns per-unit real power consumption
        calc_q(): Returns per-unit reactive power consumption
    """

    def __init__(self, name, bus1_name, mw, mvar, p=0.0, q=0.0):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Load name must be a non-empty string.")
        if not isinstance(bus1_name, str) or not bus1_name.strip():
            raise ValueError("Load bus1_name must be a non-empty string.")

        self.name = name
        self.bus1_name = bus1_name
        self.mw = float(mw)
        self.mvar = float(mvar)
        self.p = float(p)
        self.q = float(q)

    def calc_p(self):
        """Return per-unit real power consumption."""
        return self.p

    def calc_q(self):
        """Return per-unit reactive power consumption."""
        return self.q
