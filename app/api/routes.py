from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import create_access_token, set_access_cookies
from app.services.auth_service import authenticate_user
from app.services.zabbix_service import get_server_metrics
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from app.services.query_service import create_device_service, get_backup_failed_count, create_log_entry, get_logs_device, get_backup_ok_count
from app.config import Config


api_bp = Blueprint("api", __name__)

@api_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Credenciais obrigatórias"}), 400

    success = authenticate_user(username, password)

    if not success:
        return jsonify({"error": "Usuário ou senha inválidos"}), 401

    access_token = create_access_token(identity=username)

    response = jsonify({"msg": "Login OK"})
    set_access_cookies(response, access_token)

    return response

@api_bp.route("/dashboard/data", methods=["GET"])
@jwt_required()
def dashboard_data():
    data = get_server_metrics()
    backup_failed_count = get_backup_failed_count()
    backup_ok_count = get_backup_ok_count()
    data["backup_failed_count"] = backup_failed_count
    data["backup_ok_count"] = backup_ok_count
    data["logs_device"] = get_logs_device()
    return jsonify({"data": data}), 200

@api_bp.route("/create_device", methods=["POST"])
@jwt_required()
def create_device():
    data = request.get_json()
    json_response = create_device_service(data)
    if json_response[1] == 201:
        device_name = data.get("name")
        create_log_entry(device_name, action="Device criado", entity=get_jwt_identity())
    return json_response

