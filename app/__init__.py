from flask import Flask, redirect, url_for, request
from flask_jwt_extended import JWTManager
from app.config import Config

def create_app():
    app = Flask(__name__)

    from app.api.routes import api_bp
    from app.web.routes import web_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = False 
    app.config["JWT_COOKIE_HTTPONLY"] = True
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  

    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def redirect_unauthorized(reason):
        if request.path.startswith("/api"):
            return {"msg": "Token ausente ou inválido"}, 401
        return redirect(url_for("web.login"))

    return app
