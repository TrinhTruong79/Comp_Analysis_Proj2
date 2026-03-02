# transformer_m3.py
import pandas as pd


class TransformerM3:
    """
    Milestone 3 Transformer:
    - Keeps Milestone 1 parameters: name, bus1_name, bus2_name, r, x
    - Adds:
        Yseries = 1/(r + jx)
        calc_yprim() -> 2x2 primitive admittance matrix (DataFrame)
    """

    def __init__(self, name, bus1_name, bus2_name, r, x):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Transformer name must be a non-empty string.")
        if not isinstance(bus1_name, str) or not bus1_name.strip():
            raise ValueError("Transformer bus1_name must be a non-empty string.")
        if not isinstance(bus2_name, str) or not bus2_name.strip():
            raise ValueError("Transformer bus2_name must be a non-empty string.")

        self.name = name
        self.bus1_name = bus1_name
        self.bus2_name = bus2_name
        self.r = float(r)
        self.x = float(x)

        z = complex(self.r, self.x)
        if z == 0:
            raise ValueError("Transformer impedance (r + jx) cannot be zero.")
        self.Yseries = 1 / z

    def calc_yprim(self):
        """
        For a series-only 2-terminal element:
            [  y  -y ]
            [ -y   y ]
        """
        y = self.Yseries
        b1 = self.bus1_name
        b2 = self.bus2_name

        data = [
            [y, -y],
            [-y, y],
        ]
        return pd.DataFrame(data, index=[b1, b2], columns=[b1, b2])