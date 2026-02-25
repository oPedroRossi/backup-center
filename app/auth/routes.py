from flask import Blueprint, request, jsonify, g #Import blueprint, request, jsonify, g
from flask_jwt_extended import create_access_token, set_access_cookies #Import create_access_token, set_access_cookies
from app.auth.services import authenticate_user # Importa os serviços de autenticação
from app.core.config import Config # Importa a configuração do aplicativo

auth_api_bp = Blueprint("auth_api", __name__)

@auth_api_bp.route("/login", methods=["POST"])
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
    print(response.headers)
    return response