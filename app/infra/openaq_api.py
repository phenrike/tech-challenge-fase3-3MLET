# app/infra/openaq_api.py
import requests
from interfaces.sensor_repository import SensorRepository
from interfaces.measurement_repository import MeasurementRepository
from domain.models import Measurement
import numpy as np
from datetime import date, timedelta
from flask import jsonify

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
                        sensors.append({
                            "id": sensor["id"],
                            "city": location["locality"]
                        })
        return sensors

    def get_measurements(self, sensor_id: int, datetime_from: str, datetime_to: str, city: str):
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
                    city=city
                )
            )

        return measurements

class WeatherAPI():
    BASE_URL = "http://api.weatherapi.com/v1/"
    def get_history(self, city: str, date_str: str):
        """Obtém dados históricos de um determinado dia e uma cidade específica"""
        url = f"{self.BASE_URL}/history.json"
        data_obj = date.fromisoformat(date_str)
        today = date.today()
        interval = (today - data_obj).days
        data_list = []
        for i in range(interval):
            params = {"key": "3a32179cc75946e2acd01006252103", "q": city, "dt": data_obj.strftime("%Y-%m-%d")}
            response = requests.get(url, params=params)
            data = response.json()
            if response.status_code != 200:
                pass
            else:
                city = data["location"]["name"]
                date_var = data["forecast"]["forecastday"][0]["date"]
                avg_humidity = data["forecast"]["forecastday"][0]["day"]["avghumidity"]
                avg_temp_c = data["forecast"]["forecastday"][0]["day"]["avgtemp_c"]
                avg_vis_km = data["forecast"]["forecastday"][0]["day"]["avgvis_km"]
                max_wind_kph = data["forecast"]["forecastday"][0]["day"]["maxwind_kph"]
                total_precip_mm = data["forecast"]["forecastday"][0]["day"]["totalprecip_mm"]
                # extracting hour list
                hours = data["forecast"]["forecastday"][0]["hour"]
                # taking pressure_mb values and taking its mean
                pressure_mb = np.mean([hour["pressure_mb"] for hour in hours])
                #"http://127.0.0.1:5000/weather-history?city=Santiago&date=2024-03-21"
                data_list.append({
                #"city": city,
                "date": date_var,
                "avg_humidity": avg_humidity,
                "avg_temp_c": avg_temp_c,
                "avg_vis_km": avg_vis_km,
                "max_wind_kph": max_wind_kph,
                "total_precip_mm": total_precip_mm,
                "pressure_mb": pressure_mb
                })
            data_obj = data_obj + timedelta(days=1)
        #if response.status_code != 200:
        #    return []
        
        return data_list
        #return jsonify(data_list)

        
    
    def get_future(self, city: str, date: str):
        """Obtém dados da previsão do tempo de um determinado dia e uma cidade específica"""
        url = f"{self.BASE_URL}/future.json"
        params = {"key": "3a32179cc75946e2acd01006252103", "q": city, "dt": date}
        response = requests.get(url, params=params)
        print(response.status_code)
        if response.status_code != 200:
            return []

        data = response.json()
        city = data["location"]["name"]
        date_var = data["forecast"]["forecastday"][0]["date"]
        avg_humidity = data["forecast"]["forecastday"][0]["day"]["avghumidity"]
        avg_temp_c = data["forecast"]["forecastday"][0]["day"]["avgtemp_c"]
        avg_vis_km = data["forecast"]["forecastday"][0]["day"]["avgvis_km"]
        max_wind_kph = data["forecast"]["forecastday"][0]["day"]["maxwind_kph"]
        total_precip_mm = data["forecast"]["forecastday"][0]["day"]["totalprecip_mm"]
        # extracting hour list
        hours = data["forecast"]["forecastday"][0]["hour"]
        # taking pressure_mb values and taking its mean
        pressure_mb = np.mean([hour["pressure_mb"] for hour in hours])
        #"http://127.0.0.1:5000/weather-future?city=Santiago&date=2025-04-20"
        return {
        "city": city,
        "date": date_var,
        "avg_humidity": avg_humidity,
        "avg_temp_c": avg_temp_c,
        "avg_vis_km": avg_vis_km,
        "max_wind_kph": max_wind_kph,
        "total_precip_mm": total_precip_mm,
        "pressure_mb": pressure_mb
        }