from flask import Blueprint, url_for, render_template

routes_bp = Blueprint('routes', __name__)

@routes_bp.route("/")
def index():
    return "<script>window.location.href = '/kalkulasi';</script>"

@routes_bp.route("/kalkulasi")
def kalkulasi_view():
    return render_template('kalkulasi.html')

@routes_bp.route("/model-kalkulator")
def model_view():
    return render_template('kalkulator.html')
