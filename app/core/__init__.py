from flask import Flask, redirect, url_for, request
from datetime import timedelta
from app.core.config import Config
from app.core.extensions import db, migrate, jwt
import os


def create_app():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    app = Flask( __name__)

    # =========================
    # CONFIGURAÇÕES
    # =========================
    app.config.from_object(Config)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_COOKIE_HTTPONLY"] = True
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False

    # =========================
    # INICIALIZA EXTENSÕES
    # =========================
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # =========================
    # BLUEPRINTS
    # =========================
    from app.auth.routes import auth_api_bp
    from app.devices.routes import devices_api_bp
    from app.web.routes import web_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(auth_api_bp, url_prefix="/api")
    app.register_blueprint(devices_api_bp, url_prefix="/api")

    # =========================
    # HANDLERS JWT
    # =========================

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        if request.path.startswith("/api"):
            return {"msg": "Token expirado"}, 401
        return redirect(url_for("web.login"))

    @jwt.invalid_token_loader
    def invalid_token(reason):
        if request.path.startswith("/api"):
            return {"msg": "Token inválido"}, 401
        return redirect(url_for("web.login"))

    @jwt.unauthorized_loader
    def redirect_unauthorized(reason):
        if request.path.startswith("/api"):
            return {"msg": "Token ausente"}, 401
        return redirect(url_for("web.login"))

    return app