import time
from helpers.loadcells import MultiLoadCell


# Define your loadcell pins here (can also pull from .env if you want)
LOADCELL_CONFIG = [
    {"name": "loadcell1", "dout_pin": 16, "pd_sck_pin": 17},
    {"name": "loadcell2", "dout_pin": 20, "pd_sck_pin": 21},
    {"name": "loadcell3", "dout_pin": 6, "pd_sck_pin": 27},
    {"name": "loadcell4", "dout_pin": 4, "pd_sck_pin": 26},
]

def main():
    # Initialize loadcells
    loadcells = MultiLoadCell(LOADCELL_CONFIG)

    print("📟 Starting load cell test (Ctrl+C to stop)...")
    try:
        while True:
            weights = loadcells.get_all_weights()
            for name, weight in weights.items():
                print(f"{name}: {weight:.2f} g", end="  |  ")
            print()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopped test")

if __name__ == "__main__":
    main()
