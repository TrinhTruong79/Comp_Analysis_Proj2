# transmission_line_m3.py
import pandas as pd


class TransmissionLineM3:
    """
    Milestone 3 Transmission Line:
    - Keeps Milestone 1 parameters: name, bus1_name, bus2_name, r, x, g, b
    - Adds:
        Yseries = 1/(r + jx)
        Yshunt  = g + jb   (total shunt admittance)
        calc_yprim() -> 2x2 primitive admittance matrix (DataFrame)

    Pi-model stamping (shunt split equally):
        Yii = Yseries + Yshunt/2
        Yij = -Yseries
        Yji = -Yseries
        Yjj = Yseries + Yshunt/2
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

        z = complex(self.r, self.x)
        if z == 0:
            raise ValueError("Transmission line impedance (r + jx) cannot be zero.")
        self.Yseries = 1 / z
        self.Yshunt = complex(self.g, self.b)

    def calc_yprim(self):
        y = self.Yseries
        ysh = self.Yshunt
        diag = y + (ysh / 2)

        b1 = self.bus1_name
        b2 = self.bus2_name

        data = [
            [diag, -y],
            [-y, diag],
        ]
        return pd.DataFrame(data, index=[b1, b2], columns=[b1, b2])