# validate_milestone3.py
from transformer_m3 import TransformerM3
from transmission_line_m3 import TransmissionLineM3


def main():
    t = TransformerM3("T1", "Bus 1", "Bus 2", 0.01, 0.10)
    print("Transformer Yseries:")
    print(t.Yseries)
    print("Transformer Yprim:")
    print(t.calc_yprim())
    print()

    line = TransmissionLineM3("Line 1", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.04)
    print("Line Yseries, Yshunt:")
    print(line.Yseries, line.Yshunt)
    print("Line Yprim:")
    print(line.calc_yprim())
    print()


if __name__ == "__main__":
    main()