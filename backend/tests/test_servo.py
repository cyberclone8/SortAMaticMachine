import smbus2
import time

# === CONFIG ===
I2C_BUS = 3          # Software I2C bus (configured in /boot/config.txt)
PCA_ADDR = 0x40      # Default PCA9685 address
SERVO_MIN = 150      # Min pulse (adjust for your servo)
SERVO_MAX = 600      # Max pulse
STEP = 5             # Step size for sweeping
DELAY = 0.01         # Delay between steps

# === PCA9685 Registers ===
MODE1 = 0x00
LED0_ON_L = 0x06

# Initialize I2C bus
bus = smbus2.SMBus(I2C_BUS)

# Initialize PCA9685
bus.write_byte_data(PCA_ADDR, MODE1, 0x00)  # Normal mode

def set_pwm(channel, on, off):
    """Set PWM on a channel (0-15)"""
    bus.write_byte_data(PCA_ADDR, LED0_ON_L + 4*channel, on & 0xFF)
    bus.write_byte_data(PCA_ADDR, LED0_ON_L + 4*channel + 1, on >> 8)
    bus.write_byte_data(PCA_ADDR, LED0_ON_L + 4*channel + 2, off & 0xFF)
    bus.write_byte_data(PCA_ADDR, LED0_ON_L + 4*channel + 3, off >> 8)

# Sweep all 16 channels
try:
    for channel in range(16):
        print(f"Sweeping channel {channel}")
        # Sweep from min to max
        for pulse in range(SERVO_MIN, SERVO_MAX, STEP):
            set_pwm(channel, 0, pulse)
            time.sleep(DELAY)
        # Sweep back from max to min
        for pulse in range(SERVO_MAX, SERVO_MIN, -STEP):
            set_pwm(channel, 0, pulse)
            time.sleep(DELAY)
finally:
    # Turn off all channels
    for channel in range(16):
        set_pwm(channel, 0, 0)
    bus.close()
    print("Done")
