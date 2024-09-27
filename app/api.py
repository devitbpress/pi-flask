import pandas as pd

from flask import Blueprint, request, jsonify
from app.db import get_user, get_page_product, get_search_product
from app import utils

routes_api = Blueprint('api', __name__)

#  autentikasi
@routes_api.route("/get-sign", methods=['POST'])
def get_sign():
    try:
        email = request.json.get('email', "")
        password = request.json.get('password', "")

        user = get_user(email, password)

        return jsonify(user)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#  upload file
@routes_api.route("/upload-file", methods=['POST'])
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

        result = utils.processing_save_dataframe(df, request.form.get("file_id"), request.form.get("session"))
        result = result.fillna('')
        data = result.to_dict(orient='records')

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# delete file
@routes_api.route("/delete-file", methods=['POST'])
def delete_file():
    try:
        result = utils.delete_datafile(request.json.get("file_id"),request.json.get("session"))

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#  subset data
@routes_api.route("/subset", methods=['POST'])
def subset():
    try:
        result = utils.processing_subset(request.json.get("session"))
        result = result.fillna('')
        data = result.to_dict(orient='records')

        return jsonify(['success', data]), 200
    except Exception as e:
        return jsonify(['error', str(e)]), 500

#  classification data
@routes_api.route("/classification", methods=['POST'])
def classification():
    try:
        result = utils.processing_classification(request.json.get("session"))
        result = result.fillna('')
        data = result.to_dict(orient='records')

        return jsonify(['success', data]), 200
    except Exception as e:
        return jsonify(['error', str(e)]), 500

#  model calc
@routes_api.route("/model-to-calc", methods=['POST'])
def model_to_calculation():
    try:
        # df = pd.read_excel("./app/db/test.xlsx")
        result = utils.processing_model_calc(request.json.get("session"))

        return jsonify(['success', result]), 200

    except Exception as e:
        return jsonify(['error', str(e)]), 500

#  kalkulator file
@routes_api.route("/calc", methods=['POST'])
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

#  kalkulator manual
@routes_api.route("/manual-calc", methods=['POST'])
def manual_calc():
    try:
        processed_data = utils.calc_model_manual(request.form)

        return jsonify(processed_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#  ambil produk / page
@routes_api.route("/get-product", methods=['POST'])
def get_product():
    try:
        page = int(request.json.get('page', 1))
        per_page = 1000
        offset = (page - 1) * per_page

        response = get_page_product(page, per_page, offset)

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#  ambil produk / term
@routes_api.route("/search-product", methods=['POST'])
def search_product():
    try:
        search_term = request.json.get('search_term', "")
        search_term = f"%{search_term}%"

        response = get_search_product(search_term)

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#  delete session
@routes_api.route("/delete-session", methods=['POST'])
def delete_session():
    try:
        ss_id = request.json.get('session', "")
        
        response = utils.delete_session_now(ss_id)
        return jsonify(response)
    except Exception as e:
            return jsonify({'error': str(e)}), 500