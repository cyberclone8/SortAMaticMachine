try:
    from hx711 import HX711
    HX711_AVAILABLE = True
except Exception:
    HX711_AVAILABLE = False

class LoadCell:
    def __init__(self, dout_pin, pd_sck_pin, gain=128):
        self.dout = dout_pin
        self.sck = pd_sck_pin
        self.gain = gain
        self.hx = None
        self.ref_unit = 1
        if HX711_AVAILABLE:
            self.hx = HX711(dout_pin, pd_sck_pin)
            self.hx.set_reading_format("MSB", "MSB")
            self.hx.set_reference_unit(1)
            self.hx.reset()
            self.hx.tare()
        else:
            print("[SIM] HX711 library not available — load cell simulation active")

    def tare(self):
        if self.hx:
            self.hx.tare()
        else:
            print(f"[SIM] tare called for DOUT {self.dout}")

    def set_reference_unit(self, unit):
        self.ref_unit = unit
        if self.hx:
            self.hx.set_reference_unit(unit)

    def get_weight(self, times=5):
        if self.hx:
            return self.hx.get_weight(times)
        else:
            print(f"[SIM] get_weight simulated for DOUT {self.dout}")
            return 0.0
