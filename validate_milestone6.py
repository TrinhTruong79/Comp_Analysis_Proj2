# validate_milestone6.py
# Validates: Power injection equations and mismatch vector
# Uses a simple 3-bus system:
#   Bus 1 (Slack), Bus 2 (PV), Bus 3 (PQ)

import numpy as np
from bus_m5 import BusM5
from circuit_m7 import CircuitM7
from settings import Settings


def main():
    BusM5.reset_counter()

    # --- Build a simple 3-bus system ---
    settings = Settings(freq=60.0, sbase=100.0)
    c = CircuitM7("3-Bus Test System", settings)

    # Buses
    c.add_bus("Bus 1", 20.0,  bus_type="Slack", vpu=1.04, delta=0.0)
    c.add_bus("Bus 2", 230.0, bus_type="PV",    vpu=1.02, delta=0.0)
    c.add_bus("Bus 3", 230.0, bus_type="PQ",    vpu=1.00, delta=0.0)

    # Transformer: Bus 1 -- Bus 2
    c.add_transformer("T1", "Bus 1", "Bus 2", 0.01, 0.10)

    # Transmission line: Bus 2 -- Bus 3
    c.add_transmission_line("Line1", "Bus 2", "Bus 3", 0.02, 0.25, 0.0, 0.04)

    # Generator at Bus 1 (Slack), and Bus 2 (PV)
    c.add_generator("G1", "Bus 1", 1.04, 100.0, p=1.0)     # p in p.u.
    c.add_generator("G2", "Bus 2", 1.02, 50.0,  p=0.5)

    # Load at Bus 3
    c.add_load("Load1", "Bus 3", 80.0, 40.0, p=0.8, q=0.4)  # p, q in p.u.

    # Build Ybus
    c.calc_ybus()
    print("=== Ybus ===")
    print(c.ybus)
    print()

    # --- Flat start: voltages and angles ---
    bus_names = list(c.buses.keys())
    voltages = np.array([c.buses[b].vpu for b in bus_names])
    angles = np.array([np.radians(c.buses[b].delta) for b in bus_names])

    print(f"Bus names : {bus_names}")
    print(f"Voltages  : {voltages}")
    print(f"Angles(rad): {angles}")
    print()

    # --- Power injections at each bus ---
    print("=== Power Injections (flat start) ===")
    ybus_np = c.ybus.values
    for bname in bus_names:
        Pi, Qi = c.compute_power_injection(bname, ybus_np, bus_names, voltages, angles)
        print(f"  {bname}: P_calc = {Pi:+.6f}, Q_calc = {Qi:+.6f}")
    print()

    # --- Power mismatch ---
    mismatch = c.compute_power_mismatch(voltages, angles)
    print("=== Power Mismatch Vector ===")
    # Ordering: ΔP for non-slack buses, then ΔQ for PQ buses
    non_slack = [b for b in bus_names if c.buses[b].bus_type != "Slack"]
    pq_only = [b for b in bus_names if c.buses[b].bus_type == "PQ"]
    labels = [f"ΔP_{b}" for b in non_slack] + [f"ΔQ_{b}" for b in pq_only]
    for lbl, val in zip(labels, mismatch):
        print(f"  {lbl} = {val:+.6f}")
    print()

    print("Milestone 6 validation complete.")


if __name__ == "__main__":
    main()
