import RPi.GPIO as GPIO
import time

class MotorController:
    def __init__(self, en_pin, in1_pin, in2_pin):
        self.en_pin = en_pin
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.en_pin, GPIO.OUT)
        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)

        # PWM setup (1kHz)
        self.pwm = GPIO.PWM(self.en_pin, 1000)
        self.pwm.start(0)

        # ✅ Ensure motor is stopped at startup
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)
        print("Motor initialized and stopped.")

    def set_speed(self, speed):
        speed = max(0, min(100, speed))
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)
        self.pwm.ChangeDutyCycle(speed)
        print(f"Motor running at {speed}%")

    def stop(self):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)
        print("Motor stopped.")

    def cleanup(self):
        self.stop()
        self.pwm.stop()
        GPIO.cleanup([self.en_pin, self.in1_pin, self.in2_pin])
        print("GPIO cleaned up.")
