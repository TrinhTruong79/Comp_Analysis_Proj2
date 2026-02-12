from Bus import Bus
from Transformer import Transformer
from TransmissionLine import TransmissionLine
from Load import Load
from Generator import Generator


if __name__ == "__main__":

    print("===== Bus Test =====")
    bus1 = Bus("Bus-1", 20.0)
    bus2 = Bus("Bus-2", 230.0)
    print(bus1.name, bus1.nominal_kv, bus1.bus_index)
    print(bus2.name, bus2.nominal_kv, bus2.bus_index)

    print("\n===== Transformer Test =====")
    t1 = Transformer("T1", "Bus-1", "Bus-2", 0.01, 0.10)
    print(t1.name, t1.bus1_name, t1.bus2_name, t1.r, t1.x)

    print("\n===== Transmission Line Test =====")
    line1 = TransmissionLine("Line-1", "Bus-1", "Bus-2",
                             0.02, 0.25, 0.0, 0.04)
    print(line1.name, line1.bus1_name, line1.bus2_name,
          line1.r, line1.x, line1.g, line1.b)

    print("\n===== Load Test =====")
    load1 = Load("Load-1", "Bus-2", 50.0, 30.0)
    print(load1.name, load1.bus1_name, load1.mw, load1.mvar)

    print("\n===== Generator Test =====")
    gen1 = Generator("G1", "Bus-1", 1.04, 100.0)
    print(gen1.name, gen1.bus1_name,
          gen1.voltage_setpoint, gen1.mw_setpoint)