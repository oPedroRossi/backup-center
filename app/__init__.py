from flask import Flask, redirect, url_for, request
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # =========================
    # CONFIGURAÇÕES DO BANCO
    # =========================
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # =========================
    # CONFIGURAÇÕES JWT
    # =========================
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_COOKIE_HTTPONLY"] = True
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False

    # Inicializa extensões 
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)

    # =========================
    # BLUEPRINTS
    # =========================
    from app.api.routes import api_bp
    from app.web.routes import web_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

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
