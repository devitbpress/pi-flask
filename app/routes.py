from flask import Blueprint, url_for, render_template

routes_bp = Blueprint('routes', __name__)

@routes_bp.route("/")
def index():
    return f"<a href=\"{url_for('routes.name', username=123)}\">name</a>"

@routes_bp.route("/kalkulasi")
def kalkulasi_view():
    return render_template('kalkulasi.html')

@routes_bp.route("/model-kalkulator")
def model_view():
    return render_template('kalkulator.html')
