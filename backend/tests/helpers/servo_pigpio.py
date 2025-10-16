try:
    import pigpio
    PIGPIO_AVAILABLE = True
except Exception:
    pigpio = None
    PIGPIO_AVAILABLE = False

class GPIOServoController:
    def __init__(self, gpio_map):
        """
        gpio_map: dict { 'biodegradable': 12, 'non_biodegradable': 13, ... }
        """
        self.gpio_map = gpio_map
        self.pi = pigpio.pi() if PIGPIO_AVAILABLE else None

        if self.pi and self.pi.connected:
            print(f"[OK] Connected to pigpio daemon, using pins {self.gpio_map}")
        else:
            print("[SIM] pigpio not available, running in simulation mode")

    def move_servo(self, category, angle=None, microseconds=None):
        """
        Move servo for a given category.
        - angle: 0–180 (converted to 500–2500 µs pulse width)
        - microseconds: explicit pulse width
        """
        if category not in self.gpio_map:
            print(f"❌ Invalid category {category}")
            return

        gpio_pin = self.gpio_map[category]

        if microseconds is None and angle is None:
            raise ValueError("Provide either angle or microseconds")

        if microseconds is None:
            microseconds = int(500 + (angle / 180.0) * 2000)

        if self.pi and self.pi.connected:
            self.pi.set_servo_pulsewidth(gpio_pin, microseconds)
        else:
            print(f"[SIM] move_servo category={category} angle={angle} us={microseconds}")

    def cleanup(self):
        if self.pi and self.pi.connected:
            for pin in self.gpio_map.values():
                if pin > 0:
                    self.pi.set_servo_pulsewidth(pin, 0)
            self.pi.stop()
        else:
            print("[SIM] cleanup called")