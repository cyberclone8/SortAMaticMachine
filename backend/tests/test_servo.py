# pca9685_controller.py
# PCA9685 Servo Controller Module with Angle Control
# Based on I2C servo control using smbus2

import time
import smbus2


class PCA9685Controller:
    # === PCA9685 Registers ===
    MODE1 = 0x00
    LED0_ON_L = 0x06

    def __init__(
        self,
        i2c_bus: int = 3,
        address: int = 0x40,
        servo_min: int = 1000,
        servo_max: int = 2000,
        step: int = 5,
        delay: float = 0.01
    ):
        """Initialize PCA9685 controller over I2C."""
        self.i2c_bus_num = i2c_bus
        self.address = address
        self.servo_min = servo_min
        self.servo_max = servo_max
        self.step = step
        self.delay = delay

        self.bus = smbus2.SMBus(self.i2c_bus_num)
        self.bus.write_byte_data(self.address, self.MODE1, 0x00)  # Normal mode

        print(f"PCA9685 initialized at address {hex(self.address)} on I2C bus {self.i2c_bus_num}")

    def set_pwm(self, channel: int, on: int, off: int):
        """Set PWM values for a specific channel (0–15)."""
        base = self.LED0_ON_L + 4 * channel
        self.bus.write_byte_data(self.address, base, on & 0xFF)
        self.bus.write_byte_data(self.address, base + 1, on >> 8)
        self.bus.write_byte_data(self.address, base + 2, off & 0xFF)
        self.bus.write_byte_data(self.address, base + 3, off >> 8)

    def angle_to_pulse(self, angle: float) -> int:
        """
        Convert a servo angle (0–180°) to pulse width (servo_min–servo_max).
        """
        pulse_range = self.servo_max - self.servo_min
        pulse = int(self.servo_min + (angle / 180.0) * pulse_range)
        return pulse

    def move_servo(self, channel: int, angle: float):
        """
        Move a servo on the given channel to the specified angle (0–180°).
        """
        if not (0 <= angle <= 180):
            raise ValueError("Angle must be between 0 and 180 degrees.")
        pulse = self.angle_to_pulse(angle)
        self.set_pwm(channel, 0, pulse)
        print(f"Channel {channel}: moved to {angle}° (pulse {pulse})")

    # === Preset angle methods ===
    def move_to_0(self, channel: int):
        """Move servo to 0° (minimum position)."""
        self.move_servo(channel, 0)

    def move_to_90(self, channel: int):
        """Move servo to 90° (middle position)."""
        self.move_servo(channel, 90)

    def move_to_180(self, channel: int):
        """Move servo to 180° (maximum position)."""
        self.move_servo(channel, 180)

    def sweep_channel(self, channel: int):
        """Sweep a servo connected to a given channel."""
        print(f"Sweeping channel {channel}")
        # Sweep from min to max
        for pulse in range(self.servo_min, self.servo_max, self.step):
            self.set_pwm(channel, 0, pulse)
            time.sleep(self.delay)
        # Sweep from max to min
        for pulse in range(self.servo_max, self.servo_min, -self.step):
            self.set_pwm(channel, 0, pulse)
            time.sleep(self.delay)

    def sweep_all(self):
        """Sweep all 16 channels sequentially."""
        try:
            for channel in range(16):
                self.sweep_channel(channel)
        finally:
            self.stop_all()
            print("Done")

    def stop_all(self):
        """Turn off all PWM channels."""
        for channel in range(16):
            self.set_pwm(channel, 0, 0)
        self.bus.close()
        print("All channels off and I2C bus closed.")

    def __del__(self):
        """Ensure resources are released."""
        try:
            self.stop_all()
        except Exception:
            pass


if __name__ == "__main__":
    """Run basic servo test when executed directly."""
    controller = PCA9685Controller()
    try:
        channel = 0
        print("Testing servo angle positions on channel 0...")
        controller.move_to_0(channel)
        time.sleep(1)
        controller.move_to_90(channel)
        time.sleep(1)
        controller.move_to_180(channel)
        time.sleep(1)
        controller.move_to_90(channel)
        time.sleep(1)
        controller.move_to_0(channel)
    finally:
        controller.stop_all()
