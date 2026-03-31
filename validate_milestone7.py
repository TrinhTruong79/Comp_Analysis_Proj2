# validate_milestone7.py
# Validates: Jacobian matrix construction
# Uses the same 3-bus system as Milestone 6

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
    c.add_generator("G1", "Bus 1", 1.04, 100.0, p=1.0)
    c.add_generator("G2", "Bus 2", 1.02, 50.0,  p=0.5)

    # Load at Bus 3
    c.add_load("Load1", "Bus 3", 80.0, 40.0, p=0.8, q=0.4)

    # Build Ybus
    c.calc_ybus()
    print("=== Ybus ===")
    print(c.ybus)
    print()

    # --- Flat start ---
    bus_names = list(c.buses.keys())
    voltages = np.array([c.buses[b].vpu for b in bus_names])
    angles = np.array([np.radians(c.buses[b].delta) for b in bus_names])

    # --- Mismatch ---
    mismatch = c.compute_power_mismatch(voltages, angles)
    print("=== Power Mismatch Vector ===")
    non_slack = [b for b in bus_names if c.buses[b].bus_type != "Slack"]
    pq_only = [b for b in bus_names if c.buses[b].bus_type == "PQ"]
    labels = [f"ΔP_{b}" for b in non_slack] + [f"ΔQ_{b}" for b in pq_only]
    for lbl, val in zip(labels, mismatch):
        print(f"  {lbl} = {val:+.6f}")
    print()

    # --- Jacobian ---
    J = c.calc_jacobian(voltages, angles)

    # Expected dimension: (2*N - 2 - Npv) x (2*N - 2 - Npv)
    N = len(bus_names)
    Npv = sum(1 for b in c.buses.values() if b.bus_type == "PV")
    expected_dim = 2 * N - 2 - Npv
    print(f"=== Jacobian Matrix ===")
    print(f"  N = {N}, Npv = {Npv}")
    print(f"  Expected dimension: {expected_dim} x {expected_dim}")
    print(f"  Actual   dimension: {J.shape[0]} x {J.shape[1]}")
    print()

    # Label rows/cols for clarity
    row_labels = [f"∂P/∂δ_{b}" for b in non_slack] + [f"∂Q/∂δ_{b}" for b in pq_only]
    col_labels = [f"δ_{b}" for b in non_slack] + [f"|V|_{b}" for b in pq_only]

    print("Jacobian J:")
    print(f"  Rows: {row_labels}")
    print(f"  Cols: {col_labels}")
    print()

    np.set_printoptions(precision=6, suppress=True, linewidth=120)
    print(J)
    print()

    # --- Verify dimension matches mismatch vector ---
    print(f"Mismatch vector length : {len(mismatch)}")
    print(f"Jacobian rows          : {J.shape[0]}")
    assert J.shape[0] == len(mismatch), "DIMENSION MISMATCH!"
    assert J.shape[0] == J.shape[1], "Jacobian is not square!"
    print("Dimension check PASSED.")
    print()

    print("Milestone 7 validation complete.")


if __name__ == "__main__":
    main()
