from flask import Blueprint, request, jsonify, g
from app.monitoring.zabbix_service import get_server_metrics
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.devices.repository import create_device_service, get_equipament, delete_device, create_log_entry, get_logs_device, get_backup_failed_count , get_backup_ok_count

devices_api_bp = Blueprint("devices_api", __name__)

@devices_api_bp.route("/dashboard/data", methods=["GET"])
@jwt_required()
def dashboard_data():
    data = get_server_metrics()
    backup_failed_count = get_backup_failed_count()
    backup_ok_count = get_backup_ok_count()
    data["backup_failed_count"] = backup_failed_count
    data["backup_ok_count"] = backup_ok_count
    data["logs_device"] = get_logs_device()
    return jsonify({"data": data}), 200

@devices_api_bp.route("/create_device", methods=["POST"])
@jwt_required()
def create_device():
    data = request.get_json()
    json_response = create_device_service(data)
    if json_response[1] == 201:
        device_name = data.get("name")
        create_log_entry(device_name, action="Device criado", entity=get_jwt_identity())
    return json_response

@devices_api_bp.route("/equipaments/<device_type>", methods=["GET"])
@jwt_required()
def equipaments(device_type):
    data = get_equipament(device_type)
    return jsonify({"data": data}), 200

@devices_api_bp.route("/equipaments/<device_type>", methods=["DELETE"])
@jwt_required()
def delete_equipament(device_type):
    delete_device(device_type)
    return jsonify({"message": "Equipamento deletado com sucesso"}), 200