from flask import Blueprint, render_template, jsonify, url_for, request, make_response, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies

web_bp = Blueprint(
    "web",
    __name__,
    template_folder="../templates",
    static_folder="../static"
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

@web_bp.route("/telefonia")
@jwt_required()
def telefonia():
    return render_template("equipamentos.html")

@web_bp.route("/switchs")
@jwt_required()
def switchs():
    return render_template("equipamentos.html")

@web_bp.route("/firewall")
@jwt_required()
def firewall():
    return render_template("equipamentos.html")

@web_bp.route("/cadastro")
@jwt_required()
def cadastro():
    return render_template("form.html")