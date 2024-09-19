from flask import Blueprint, url_for, render_template, request, jsonify
from app import utils
import pandas as pd
import traceback

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

@routes_bp.route("/database")
def database_view():
    return render_template('database.html')

@routes_bp.route("/testing")
def testing_view():
    return render_template('testing.html')

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
    
@routes_bp.route("/save-dataframe", methods=['POST'])
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
    
@routes_bp.route("/kalkulasi-model")
def analyst_view():
    return render_template('analyst-ui.html')

@routes_bp.route("/upload-file", methods=['POST'])
def check_file():
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
