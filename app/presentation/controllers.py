from flask import Blueprint, jsonify
from application.services import SensorService
from infra.openaq_api import OpenAQApi

sensor_bp = Blueprint("sensor", __name__)

@sensor_bp.route("/sensors/pm25/chile", methods=["GET"])
def get_pm25_sensors():
    service = SensorService(OpenAQApi())
    sensors = service.get_pm25_sensors()
    return jsonify({"pm25_sensors": sensors})