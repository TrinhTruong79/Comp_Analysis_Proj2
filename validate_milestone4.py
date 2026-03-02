# validate_milestone4.py
from bus import Bus
from circuit_m4 import CircuitM4


def main():
    Bus.reset_counter()

    c = CircuitM4("Milestone 4 Test")
    c.add_bus("Bus 1", 20.0)
    c.add_bus("Bus 2", 230.0)

    c.add_transformer("T1", "Bus 1", "Bus 2", 0.01, 0.10)
    c.add_transmission_line("Line 1", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.04)

    c.calc_ybus()

    print("Ybus:")
    print(c.ybus)


if __name__ == "__main__":
    main()