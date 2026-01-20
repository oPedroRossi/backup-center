from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies
from app.services.auth_service import authenticate_user
from app.services.zabbix_service import get_server_metrics

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
def dashboard_data():
    data = get_server_metrics()
    print(data)
    return jsonify({"data": data}), 200