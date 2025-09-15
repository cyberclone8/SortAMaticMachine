import time
from helpers.l298n_motor import L298NConveyor

# Update pins if different
EN_PIN = 18
IN1_PIN = 23
IN2_PIN = 24

def main():
    conveyor = L298NConveyor(en_pin=EN_PIN, in1_pin=IN1_PIN, in2_pin=IN2_PIN)

    print("⚡ Local conveyor motor test (Ctrl+C to stop)")

    try:
        # Step 1: Start at 50%
        print("➡️ Starting conveyor at 50% speed for 3 seconds")
        conveyor.set_speed(50)
        time.sleep(3)

        # Step 2: Increase to 100%
        print("➡️ Increasing speed to 100% for 3 seconds")
        conveyor.set_speed(100)
        time.sleep(3)

        # Step 3: Stop
        print("🛑 Stopping conveyor for 2 seconds")
        conveyor.stop()
        time.sleep(2)

        # Step 4: Reverse (if implemented in L298NConveyor)
        print("↩️ Running conveyor in reverse at 50% speed for 3 seconds")
        conveyor.set_speed(-50)  # assumes negative = reverse
        time.sleep(3)

        # Final stop
        print("🛑 Final stop")
        conveyor.stop()

    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user, stopping conveyor")
        conveyor.stop()

if __name__ == "__main__":
    main()