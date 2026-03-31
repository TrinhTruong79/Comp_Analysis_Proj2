# validate_milestone5.py
# Validates: Settings, BusM5, GeneratorM5, LoadM5

from settings import Settings
from bus_m5 import BusM5
from generator_m5 import GeneratorM5
from load_m5 import LoadM5


def main():
    # --- Settings ---
    print("=== Settings Class ===")
    s = Settings()
    print(f"  freq  = {s.freq} Hz")
    print(f"  sbase = {s.sbase} MVA")

    s2 = Settings(freq=50.0, sbase=200.0)
    print(f"  Custom: freq={s2.freq}, sbase={s2.sbase}")
    print()

    # --- Bus ---
    print("=== BusM5 Class ===")
    BusM5.reset_counter()

    b1 = BusM5("Bus 1", 20.0, bus_type="Slack", vpu=1.04, delta=0.0)
    print(f"  {b1.name}: kv={b1.nominal_kv}, type={b1.bus_type}, "
          f"vpu={b1.vpu}, delta={b1.delta}, index={b1.bus_index}")

    b2 = BusM5("Bus 2", 230.0, bus_type="PV", vpu=1.02, delta=0.0)
    print(f"  {b2.name}: kv={b2.nominal_kv}, type={b2.bus_type}, "
          f"vpu={b2.vpu}, delta={b2.delta}, index={b2.bus_index}")

    b3 = BusM5("Bus 3", 230.0, bus_type="PQ")
    print(f"  {b3.name}: kv={b3.nominal_kv}, type={b3.bus_type}, "
          f"vpu={b3.vpu}, delta={b3.delta}, index={b3.bus_index}")

    # Invalid bus_type should raise an error
    try:
        BusM5("Bad Bus", 100.0, bus_type="Invalid")
    except ValueError as e:
        print(f"  Expected error: {e}")
    print()

    # --- Generator ---
    print("=== GeneratorM5 Class ===")
    g1 = GeneratorM5("G1", "Bus 1", 1.04, 100.0, p=1.0)
    print(f"  {g1.name}: bus={g1.bus1_name}, Vset={g1.voltage_setpoint}, "
          f"MW={g1.mw_setpoint}, p(pu)={g1.p}, calc_p()={g1.calc_p()}")
    print()

    # --- Load ---
    print("=== LoadM5 Class ===")
    ld1 = LoadM5("Load 1", "Bus 3", 50.0, 30.0, p=0.5, q=0.3)
    print(f"  {ld1.name}: bus={ld1.bus1_name}, MW={ld1.mw}, MVAR={ld1.mvar}, "
          f"p(pu)={ld1.p}, q(pu)={ld1.q}")
    print(f"  calc_p()={ld1.calc_p()}, calc_q()={ld1.calc_q()}")
    print()

    print("Milestone 5 validation complete.")


if __name__ == "__main__":
    main()
