import time
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except Exception:
    GPIO_AVAILABLE = False

class L298NConveyor:
    def __init__(self, en_pin, in1_pin, in2_pin, pwm_frequency=1000):
        self.en = en_pin
        self.in1 = in1_pin
        self.in2 = in2_pin
        self.pwm_freq = pwm_frequency
        self.pwm = None
        if GPIO_AVAILABLE:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.en, GPIO.OUT)
            GPIO.setup(self.in1, GPIO.OUT)
            GPIO.setup(self.in2, GPIO.OUT)
            self.pwm = GPIO.PWM(self.en, self.pwm_freq)
            self.pwm.start(0)
        else:
            print("[SIM] RPi.GPIO not available — conveyor in simulation mode")

    def set_speed(self, speed_percent: float):
        speed = max(-100.0, min(100.0, speed_percent))
        if GPIO_AVAILABLE and self.pwm:
            if speed >= 0:
                GPIO.output(self.in1, GPIO.HIGH)
                GPIO.output(self.in2, GPIO.LOW)
                self.pwm.ChangeDutyCycle(speed)
            else:
                GPIO.output(self.in1, GPIO.LOW)
                GPIO.output(self.in2, GPIO.HIGH)
                self.pwm.ChangeDutyCycle(-speed)
        else:
            print(f"[SIM] set_speed {speed}%")

    def stop(self):
        if GPIO_AVAILABLE and self.pwm:
            self.pwm.ChangeDutyCycle(0)
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.LOW)
        else:
            print("[SIM] conveyor stop")

    def cleanup(self):
        if GPIO_AVAILABLE:
            self.pwm.stop()
            GPIO.cleanup()
