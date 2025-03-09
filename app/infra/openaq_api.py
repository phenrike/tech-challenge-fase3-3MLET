# app/infra/openaq_api.py
import requests
from interfaces.sensor_repository import SensorRepository
from interfaces.measurement_repository import MeasurementRepository
from domain.models import Measurement

class OpenAQApi(SensorRepository, MeasurementRepository):
    BASE_URL = "https://api.openaq.org/v3"
    HEADERS = {"accept": "application/json", "X-API-Key": "ecc5b9ce27bba10c7c2cf36a3c2c859063a63239ebc48652688d37e3782aeac6"}

    def get_pm25_sensors_from_chile(self):
        """ Obtém os sensores de PM2.5 no Chile """
        url = f"{self.BASE_URL}/locations"
        params = {"limit": 100, "page": 1, "order_by": "id", "sort_order": "asc"}
        response = requests.get(url, headers=self.HEADERS, params=params)
        data = response.json()

        sensors = []
        for location in data.get("results", []):
            if location.get("country", {}).get("code") == "CL":
                for sensor in location.get("sensors", []):
                    if sensor.get("parameter", {}).get("name") == "pm25":
                        sensors.append(sensor["id"])
        return sensors

    def get_measurements(self, sensor_id: int, datetime_from: str, datetime_to: str):
        """ Obtém medições de um sensor específico """
        url = f"{self.BASE_URL}/sensors/{sensor_id}/measurements/daily"
        params = {"datetime_from": datetime_from, "datetime_to": datetime_to, "limit": 100}
        response = requests.get(url, headers=self.HEADERS, params=params)

        if response.status_code != 200:
            return []

        data = response.json()
        measurements = []

        for result in data.get("results", []):
            measurements.append(
                Measurement(
                    sensor_id=sensor_id,
                    value=result["value"],
                    datetime_from=result["period"]["datetimeFrom"]["local"],
                    datetime_to=result["period"]["datetimeTo"]["local"],
                )
            )

        return measurements
