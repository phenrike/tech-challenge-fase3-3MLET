from infra.openaq_api import OpenAQApi

class SensorService:
    def __init__(self, repository: OpenAQApi):
        self.repository = repository

    def get_pm25_sensors(self):
        return self.repository.get_pm25_sensors_from_chile()