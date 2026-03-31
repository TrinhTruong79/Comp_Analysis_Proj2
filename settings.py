# settings.py
# Milestone 5: System Settings Class


class Settings:
    """
    Centralized system-wide per-unit parameters.

    Attributes:
        freq  : System frequency in Hz (default 60)
        sbase : System base apparent power in MVA (default 100)
    """

    def __init__(self, freq=60.0, sbase=100.0):
        self.freq = float(freq)
        self.sbase = float(sbase)
