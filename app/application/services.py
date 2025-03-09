# app/application/services.py
from infra.openaq_api import OpenAQApi

class SensorService:
    def __init__(self, repository: OpenAQApi):
        self.repository = repository

    def get_pm25_sensors(self):
        return self.repository.get_pm25_sensors_from_chile()

class MeasurementService:
    def __init__(self, repository: OpenAQApi):
        self.repository = repository

    def get_measurements_for_all_sensors(self, datetime_from: str, datetime_to: str):
        sensor_service = SensorService(self.repository)
        sensor_ids = sensor_service.get_pm25_sensors()

        if not sensor_ids:
            return []

        measurements = []
        for sensor_id in sensor_ids:
            measurements.extend(self.repository.get_measurements(sensor_id, datetime_from, datetime_to))

        return measurements
