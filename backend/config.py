import os
from dotenv import load_dotenv

load_dotenv()

def get_servo_gpio_config():
    return {
        "biodegradable": int(os.getenv("SERVO_BIO", 12)),
        "non_biodegradable": int(os.getenv("SERVO_NONBIO", 13)),
        "recyclable": int(os.getenv("SERVO_REC", 18)),
        "paper": int(os.getenv("SERVO_PAPER", 19)),
        "spare": int(os.getenv("SERVO_SPARE", 0)),  # optional
    }