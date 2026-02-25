from flask import Blueprint, render_template, jsonify, url_for, request, make_response, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

web_bp = Blueprint(
    "web",
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
    static_url_path="/web_static"
)

@web_bp.route("/login")
def login():
    return render_template("login.html")

@web_bp.route("/logout")
def logout():
    response = make_response(redirect(url_for("web.login")))
    unset_jwt_cookies(response)
    return response

@web_bp.route("/")
@jwt_required()
def index():
    return render_template("dashboard.html")

@web_bp.route("/equipaments/<equipament_type>")
@jwt_required()
def telefonia(equipament_type):
    return render_template("equipament.html", equipament_type=equipament_type)

@web_bp.route("/cadastro")
@jwt_required()
def cadastro():
    return render_template("form.html")