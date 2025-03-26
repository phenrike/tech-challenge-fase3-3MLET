# app/presentation/controllers.py
from flask import Blueprint, jsonify, request
from application.services import SensorService, MeasurementService, HistoryService, FutureService
from infra.openaq_api import OpenAQApi, WeatherAPI

sensor_bp = Blueprint("sensor", __name__)
weather_bp = Blueprint("weather", __name__)

@sensor_bp.route("/sensors/pm25/chile", methods=["GET"])
def get_pm25_sensors():
    service = SensorService(OpenAQApi())
    sensors = service.get_pm25_sensors()
    return jsonify({"pm25_sensors": sensors})

@sensor_bp.route("/sensor-data", methods=["GET"])
def get_sensor_measurements():
    datetime_from = request.args.get("datetime_from")
    datetime_to = request.args.get("datetime_to")

    if not datetime_from or not datetime_to:
        return jsonify({"error": "Parâmetros 'datetime_from' e 'datetime_to' são obrigatórios"}), 400

    service = MeasurementService(OpenAQApi())
    measurements = service.get_measurements_for_all_sensors(datetime_from, datetime_to)

    return jsonify([{
        "sensor_id": m.sensor_id,
        "value": m.value,
        "datetimeFrom_local": m.datetime_from,
        "datetimeTo_local": m.datetime_to,
        "city": m.city
    } for m in measurements])

@weather_bp.route("/weather-history", methods=["GET"])
def get_weather_history():
    city = request.args.get("city")
    date = request.args.get("date")

    if not city or not date:
        return jsonify({"error": "Parâmetros 'city' e 'date' são obrigatórios"}), 400

    service = HistoryService(WeatherAPI())
    resp = service.get_city_history(city, date)

    return jsonify({"data": resp})

@weather_bp.route("/weather-future", methods=["GET"])
def get_weather_future():
    city = request.args.get("city")
    date = request.args.get("date")

    if not city or not date:
        return jsonify({"error": "Parâmetros 'city' e 'date' são obrigatórios"}), 400

    service = FutureService(WeatherAPI())
    resp = service.get_city_future(city, date)

    return jsonify({"data": resp})