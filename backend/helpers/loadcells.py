from .hx711_loadcell import LoadCell

class MultiLoadCell:
    def __init__(self, configs):
        self.sensors = {}
        for cfg in configs:
            self.sensors[cfg['name']] = LoadCell(
                dout_pin=cfg['dout_pin'],
                pd_sck_pin=cfg['pd_sck_pin']
            )

    def get_all_weights(self):
        return {name: sensor.get_weight() for name, sensor in self.sensors.items()}

    def tare_all(self):
        for sensor in self.sensors.values():
            sensor.tare()
