from flask import Blueprint, url_for, render_template, request, jsonify, session, flash, redirect
from app import utils
from werkzeug.security import check_password_hash
import pandas as pd
import traceback
import pymysql

routes_bp = Blueprint('routes', __name__)

def get_db_connection():
    return pymysql.connect(
            host='localhost',
            user='alisatia',
            password='@[db_aliSatia#9]',
            database='itbpress_erp',
            cursorclass=pymysql.cursors.DictCursor
    )

@routes_bp.route("/")
def index():
    return "<script>window.location.href = '/kalkulasi-model';</script>"

@routes_bp.route("/delete-kalkulasi")
def kalkulasi_view():
    return "<script>window.location.href = '/kalkulasi-model';</script>"

@routes_bp.route("/delete-model-kalkulator")
def model_view():
    return render_template('kalkulator.html')

@routes_bp.route("/delete-database")
def database_view():
    return render_template('database.html')

@routes_bp.route("/delete-testing")
def testing_view():
    return render_template('testing.html')

@routes_bp.route("/delete-save-dataframe", methods=['POST'])
def save_dataframe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.endswith(('.xls', '.xlsx')):
        return jsonify({'error': 'Invalid file format. Only .xls and .xlsx files are allowed.'}), 400

    if file.content_type not in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
        return jsonify({'error': 'Invalid file format. Only Excel files are allowed.'}), 400
    
    try:
        df = pd.read_excel(file, engine='openpyxl')

        result = utils.processing_save_dataframe(df, request.form.get("numid"), request.form.get("session"))
        result = result.fillna('')
        data = result.to_dict(orient='records')
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@routes_bp.route("/kalkulasi-model")
def analyst_view():
    return render_template('analyst-ui.html')

@routes_bp.route("/kalkulator-model")
def calc_view():
    return render_template('calc-ui.html')

@routes_bp.route("/produk")
def product_view():
    return render_template('product-ui.html')

@routes_bp.route("/masuk")
def login_view():
    return render_template('login-ui.html')

@routes_bp.route("/upload-file", methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang diunggah'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Tidak ada file yang diunggah'}), 400

    if not file.filename.endswith(('.xls', '.xlsx', '.XLS', '.XLSX')):
        return jsonify({'error': 'Format file tidak valid'}), 400

    if file.content_type not in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
        return jsonify({'error': 'Format file tidak valid'}), 400
    
    try:
        df = pd.read_excel(file, engine='openpyxl')

        result = utils.processing_save_dataframe(df, request.form.get("numid"), request.form.get("session"))
        result = result.fillna('')
        data = result.to_dict(orient='records')

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_bp.route("/delete-file", methods=['POST'])
def delete_file():
    try:
        result = utils.delete_datafile(request.form.get("numid"),request.form.get("session"))

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_bp.route("/subset", methods=['POST'])
def subset():
    try:
        result = utils.processing_subset(request.form.get("session"))
        result = result.fillna('')
        data = result.to_dict(orient='records')

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_bp.route("/classification", methods=['POST'])
def classification():
    try:
        result = utils.processing_classification(request.form.get("session"))
        result = result.fillna('')
        data = result.to_dict(orient='records')

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_bp.route("/calc", methods=['POST'])
def calc():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.endswith(('.xls', '.xlsx')):
        return jsonify({'error': 'Invalid file format. Only .xls and .xlsx files are allowed.'}), 400

    if file.content_type not in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
        return jsonify({'error': 'Invalid file format. Only Excel files are allowed.'}), 400

    model = request.form.get('model', 'none')
    
    try:
        df = pd.read_excel(file, engine='openpyxl')
        df = df.fillna('')
        data = df.to_dict(orient='records')
        
        processed_data = utils.calc_model(data, model)
        
        return jsonify(processed_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_bp.route("/manual-calc", methods=['POST'])
def manual_calc():
    try:
        processed_data = utils.calc_model_manual(request.form)

        return jsonify(processed_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@routes_bp.route("/get-product", methods=['POST'])
def get_product():
    try:
        page = int(request.json.get('page', 1))
        per_page = 1000
        offset = (page - 1) * per_page
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql_products = "SELECT * FROM pi_product LIMIT %s OFFSET %s"
            cursor.execute(sql_products, (per_page, offset))
            products = cursor.fetchall()
            
            sql_total_pages = "SELECT CEIL(COUNT(*) / %s) AS total_pages FROM pi_product"
            cursor.execute(sql_total_pages, (per_page,))
            total_pages = cursor.fetchone()['total_pages']
        
        connection.close()
        
        return jsonify({
            'products': products,
            'total_pages': total_pages,
            'current_page': page
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@routes_bp.route("/search-product", methods=['POST'])
def search_product():
    try:
        search_term = request.json.get('search_term', "")
        search_term = f"%{search_term}%"
        
        connection = get_db_connection()
        with connection.cursor() as cursor: 
            sql = """
            SELECT * FROM `pi_product` WHERE `p_code` LIKE %s OR `p_description` LIKE %s OR `p_price` LIKE %s
            """
            cursor.execute(sql, (search_term, search_term, search_term))
            
            columns = [column[0] for column in cursor.description]
            products = cursor.fetchall()

        connection.close()
        return jsonify(products)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE email = %s"
                cursor.execute(sql, (email,))
                user = cursor.fetchone()
        finally:
            connection.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash('Login successful!', 'success')
            return redirect(url_for('routes_bp.login'))
        else:
            flash('Invalid email or password', 'danger')
            
    return render_template('login-ui.html')