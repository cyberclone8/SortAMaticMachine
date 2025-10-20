import smbus2
import time

class PCA9685Controller:
    # PCA9685 register definitions
    MODE1 = 0x00
    LED0_ON_L = 0x06
    PRESCALE = 0xFE

    def __init__(self, i2c_bus=3, address=0x40, servo_min_us=500, servo_max_us=2500, freq_hz=50):
        self.address = address
        self.i2c_bus_num = i2c_bus
        self.bus = smbus2.SMBus(self.i2c_bus_num)
        self.freq_hz = freq_hz
        self.servo_min_us = servo_min_us
        self.servo_max_us = servo_max_us

        # Initialize PCA9685
        self.bus.write_byte_data(self.address, self.MODE1, 0x00)  # normal mode
        self.set_pwm_freq(self.freq_hz)

        print(f"PCA9685 initialized at address 0x{self.address:02X} on I2C bus {self.i2c_bus_num}")
        print(f"Servo pulse range: {self.servo_min_us}-{self.servo_max_us} µs @ {self.freq_hz} Hz")

    def set_pwm_freq(self, freq_hz):
        """Set the PWM frequency for all channels (default 50 Hz for servos)."""
        prescale_val = int(round(25000000.0 / (4096 * freq_hz) - 1))
        old_mode = self.bus.read_byte_data(self.address, self.MODE1)
        new_mode = (old_mode & 0x7F) | 0x10  # sleep
        self.bus.write_byte_data(self.address, self.MODE1, new_mode)
        self.bus.write_byte_data(self.address, self.PRESCALE, prescale_val)
        self.bus.write_byte_data(self.address, self.MODE1, old_mode)
        time.sleep(0.005)
        self.bus.write_byte_data(self.address, self.MODE1, old_mode | 0xA1)  # restart
        print(f"PWM frequency set to {freq_hz} Hz (prescale={prescale_val})")

    def set_pwm(self, channel, on, off):
        """Low-level: Set PWM on/off ticks for a channel (0–15)."""
        base = self.LED0_ON_L + 4 * channel
        self.bus.write_byte_data(self.address, base, on & 0xFF)
        self.bus.write_byte_data(self.address, base + 1, on >> 8)
        self.bus.write_byte_data(self.address, base + 2, off & 0xFF)
        self.bus.write_byte_data(self.address, base + 3, off >> 8)

    def angle_to_ticks(self, angle):
        """Convert 0–180° angle to PCA9685 ticks."""
        pulse_us = (self.servo_min_us +
                    (self.servo_max_us - self.servo_min_us) * (angle / 180.0))
        pulse_length_us = 1000000.0 / self.freq_hz / 4096.0
        ticks = int(pulse_us / pulse_length_us)
        return max(0, min(4095, ticks))

    def move_servo(self, channel, angle, release_after=False):
        """Move a servo to a specified angle (0–180°)."""
        ticks = self.angle_to_ticks(angle)
        self.set_pwm(channel, 0, ticks)
        print(f"Servo channel {channel} → {angle}° ({ticks} ticks)")
        if release_after:
            time.sleep(0.5)
            self.set_pwm(channel, 0, 0)

    def move_to_0(self, channel): self.move_servo(channel, 0)
    def move_to_90(self, channel): self.move_servo(channel, 90)
    def move_to_180(self, channel): self.move_servo(channel, 180)

    def stop_all(self):
        """Turn off all channels (set PWM = 0)."""
        for ch in range(16):
            self.set_pwm(ch, 0, 0)
        print("All channels off and I2C bus closed.")
        self.bus.close()


if __name__ == "__main__":
    # Simple standalone test (sweeps channel 0)
    servo = PCA9685Controller()
    try:
        while True:
            servo.move_to_0(0)
            time.sleep(1)
            servo.move_to_90(0)
            time.sleep(1)
            servo.move_to_180(0)
            time.sleep(1)
    except KeyboardInterrupt:
        servo.stop_all()
