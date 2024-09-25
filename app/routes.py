from flask import Blueprint, url_for, render_template

routes_bp = Blueprint('routes', __name__)

# base
@routes_bp.route("/")
def index():
    return "<script>window.location.href = '/kalkulasi-model';</script>"

# halaman kalkulasi
@routes_bp.route("/kalkulasi-model")
def analyst_view():
    return render_template('analyst-ui.html')

# halaman kalkulator
@routes_bp.route("/kalkulator-model")
def calc_view():
    return render_template('calc-ui.html')

# route halaman produk
@routes_bp.route("/produk")
def product_view():
    return render_template('product-ui.html')

# halaman login
@routes_bp.route("/masuk")
def login_view():
    return render_template('login-ui.html')
