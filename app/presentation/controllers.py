# app/presentation/controllers.py
from flask import Blueprint, jsonify, request
from application.services import SensorService, MeasurementService, HistoryService, FutureService, OrchestratorService
from infra.openaq_api import OpenAQApi, WeatherAPI
from infra.database import Database
import pandas as pd
import pickle
from sqlalchemy import create_engine
from sklearn.preprocessing import OneHotEncoder

sensor_bp = Blueprint("sensor", __name__)
weather_bp = Blueprint("weather", __name__)
orchestrator_bp = Blueprint("orchestrator", __name__)

# Instância global do OrchestratorService
_orchestrator = None

def get_orchestrator():
    global _orchestrator
    if _orchestrator is None:
        measurement_service = MeasurementService(OpenAQApi())
        history_service = HistoryService(WeatherAPI())
        database = Database()
        _orchestrator = OrchestratorService(measurement_service, history_service, database)
    return _orchestrator

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

@orchestrator_bp.route("/orchestrator", methods=["POST"])
def process_and_save_data():
    try:
        datetime_from = "2024-04-03T00:00:00Z"
        datetime_to = "2025-04-03T00:00:00Z"
        
        orchestrator = get_orchestrator()
        result = orchestrator.process_and_save_data(datetime_from, datetime_to)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@orchestrator_bp.route("/orchestrator/progress", methods=["GET"])
def get_progress():
    orchestrator = get_orchestrator()
    return jsonify(orchestrator.get_progress())


@weather_bp.route("/forecast_pm25", methods=["GET"])
def forecast_pm25():
    city = request.args.get("city")
    date = request.args.get("date")

    if not city or not date:
        return jsonify({"error": "Parâmetros 'city' e 'date' são obrigatórios"}), 400

    service = WeatherAPI()
    forecast = service.forecast_pm25(city, date)

    #if not forecast:
    #    return jsonify({"error": "Não foi possível gerar a previsão de PM2.5"}), 404

    return forecast

    #return jsonify({"data": forecast})