import pigpio
import time

# Servo GPIO pins
SERVO_PINS = [12, 13, 18, 19]

# Pulse width range (adjust if your servos need different min/max)
MIN_PW = 500   # 0 degrees
MAX_PW = 2500  # 180 degrees
MID_PW = 1500  # ~90 degrees

def test_servos():
    pi = pigpio.pi()
    if not pi.connected:
        print("❌ Could not connect to pigpio daemon. Did you run 'sudo systemctl start pigpiod'?")
        return

    try:
        for pin in SERVO_PINS:
            print(f"Testing servo on GPIO {pin}...")

            # Center position
            pi.set_servo_pulsewidth(pin, MID_PW)
            time.sleep(1)

            # Sweep from min → max
            pi.set_servo_pulsewidth(pin, MIN_PW)
            time.sleep(1)

            pi.set_servo_pulsewidth(pin, MAX_PW)
            time.sleep(1)

            # Back to center
            pi.set_servo_pulsewidth(pin, MID_PW)
            time.sleep(1)

            # Stop signal to avoid jitter
            pi.set_servo_pulsewidth(pin, 0)
            print(f"✅ Finished testing GPIO {pin}\n")

    finally:
        # Cleanup all pins
        for pin in SERVO_PINS:
            pi.set_servo_pulsewidth(pin, 0)
        pi.stop()

if __name__ == "__main__":
    test_servos()