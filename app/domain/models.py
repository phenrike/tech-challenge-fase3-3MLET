# app/domain/models.py
class Sensor:
    def __init__(self, sensor_id: int, name: str):
        self.sensor_id = sensor_id
        self.name = name

class Measurement:
    def __init__(self, sensor_id: int, value: float, datetime_from: str, datetime_to: str):
        self.sensor_id = sensor_id
        self.value = value
        self.datetime_from = datetime_from
        self.datetime_to = datetime_to
