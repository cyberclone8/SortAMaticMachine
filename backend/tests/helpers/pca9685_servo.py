try:
    import board
    import busio
    from adafruit_pca9685 import PCA9685
    from adafruit_motor import servo as adafruit_servo
    ADAPTER_AVAILABLE = True
except Exception:
    PCA9685 = None
    ADAPTER_AVAILABLE = False

class PCA9685ServoController:
    def __init__(self, i2c_bus=None, address=0x40, frequency=50):
        self.address = address
        self.frequency = frequency
        self.pca = None
        if ADAPTER_AVAILABLE:
            i2c = i2c_bus or busio.I2C(board.SCL, board.SDA)
            self.pca = PCA9685(i2c, address=self.address)
            self.pca.frequency = self.frequency
        else:
            print("[SIM] PCA9685 not available, running in simulation mode")

    def move_servo(self, channel, angle=None, microseconds=None):
        """Move servo either by angle (0-180) or pulse width in microseconds.
        In simulation mode this prints the action."""
        if microseconds is None and angle is None:
            raise ValueError('Provide angle or microseconds')
        if microseconds is None:
            microseconds = 1000 + (angle / 180.0) * 1000
        if self.pca:
            # Convert microseconds to duty_cycle 0..0xFFFF for adafruit_motor servo helper
            pulse_length = 1000000.0 / self.frequency
            duty = int((microseconds / pulse_length) * 0x10000)
            self.pca.channels[channel].duty_cycle = duty
        else:
            print(f"[SIM] move_servo ch={channel} angle={angle} us={microseconds}")
