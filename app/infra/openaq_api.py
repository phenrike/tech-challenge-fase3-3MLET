import requests
from interfaces.sensor_repository import SensorRepository

class OpenAQApi(SensorRepository):
    BASE_URL = "https://api.openaq.org/v3/locations"
    HEADERS = {"accept": "application/json", "X-API-Key": "ecc5b9ce27bba10c7c2cf36a3c2c859063a63239ebc48652688d37e3782aeac6"}

    def get_pm25_sensors_from_chile(self):
        params = {"limit": 100, "page": 1, "order_by": "id", "sort_order": "asc"}
        response = requests.get(self.BASE_URL, headers=self.HEADERS, params=params)
        data = response.json()

        sensors = []
        for location in data.get("results", []):
            if location.get("country", {}).get("code") == "CL":
                for sensor in location.get("sensors", []):
                    if sensor.get("parameter", {}).get("name") == "pm25":
                        sensors.append(sensor["id"])
        return sensors
