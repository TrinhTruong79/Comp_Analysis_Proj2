# validate_milestone1.py
from bus import Bus
from transformer import Transformer
from transmission_line import TransmissionLine
from load import Load
from generator import Generator


def main():
    Bus.reset_counter()

    b1 = Bus("Bus 1", 20.0)
    b2 = Bus("Bus 2", 230.0)
    print("Bus Example:")
    print(b1.name, b1.nominal_kv, b1.bus_index)
    print(b2.name, b2.nominal_kv, b2.bus_index)
    print()

    t1 = Transformer("T1", "Bus 1", "Bus 2", 0.01, 0.10)
    print("Transformer Example:")
    print(t1.name, t1.bus1_name, t1.bus2_name, t1.r, t1.x)
    print()

    line1 = TransmissionLine("Line 1", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.04)
    print("Transmission Line Example:")
    print(line1.name, line1.bus1_name, line1.bus2_name, line1.r, line1.x, line1.g, line1.b)
    print()

    load1 = Load("Load 1", "Bus 2", 50.0, 30.0)
    print("Load Example:")
    print(load1.name, load1.bus1_name, load1.mw, load1.mvar)
    print()

    g1 = Generator("G1", "Bus 1", 1.04, 100.0)
    print("Generator Example:")
    print(g1.name, g1.bus1_name, g1.voltage_setpoint, g1.mw_setpoint)


if __name__ == "__main__":
    main()