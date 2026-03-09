from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Server is running'})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload .xlsx or .xls files'}), 400
        
        # Read the Excel file directly from memory
        df = pd.read_excel(file)
        
        # Get column names
        columns = df.columns.tolist()
        
        # Get preview data (first 10 rows)
        preview_data = df.head(10).to_dict('records')
        
        # Convert NaN to None for JSON serialization
        for row in preview_data:
            for key, value in row.items():
                if pd.isna(value):
                    row[key] = None
        
        return jsonify({
            'columns': columns,
            'preview': preview_data,
            'totalRows': len(df),
            'message': 'File uploaded successfully'
        })
    
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/api/calculate', methods=['POST'])
def calculate_interest_rate():
    try:
        data = request.json
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        principal_col = data.get('principalColumn')
        interest_col = data.get('interestColumn')
        interest_type = data.get('interestType', 'amount')
        
        if not principal_col or not interest_col:
            return jsonify({'error': 'Please specify principal and interest columns'}), 400
        
        # Read the Excel file
        df = pd.read_excel(file)
        
        # Extract columns
        principal = pd.to_numeric(df[principal_col], errors='coerce')
        interest = pd.to_numeric(df[interest_col], errors='coerce')
        
        # Remove invalid rows
        valid_mask = (~principal.isna()) & (~interest.isna()) & (principal != 0)
        principal_clean = principal[valid_mask]
        interest_clean = interest[valid_mask]
        
        if len(principal_clean) == 0:
            return jsonify({'error': 'No valid data found'}), 400
        
        # Calculate interest rates
        if interest_type == 'amount':
            interest_rates = (interest_clean / principal_clean) * 100
        else:
            interest_rates = interest_clean
        
        # Prepare detailed breakdown
        breakdown = []
        for i, (idx, rate) in enumerate(zip(valid_mask[valid_mask].index, interest_rates)):
            breakdown.append({
                'row': int(idx) + 1,
                'principal': float(principal_clean.iloc[i]),
                'interest': float(interest_clean.iloc[i]),
                'rate': float(rate)
            })
        
        # Calculate statistics
        result = {
            'average': float(interest_rates.mean()),
            'median': float(interest_rates.median()),
            'min': float(interest_rates.min()),
            'max': float(interest_rates.max()),
            'stdDev': float(interest_rates.std()),
            'count': int(len(interest_rates)),
            'breakdown': breakdown
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Error calculating interest rate: {str(e)}'}), 500

@app.route('/api/calculate-from-data', methods=['POST'])
def calculate_from_data():
    try:
        data = request.json
        
        file_data = data.get('fileData')
        principal_col = data.get('principalColumn')
        interest_col = data.get('interestColumn')
        interest_type = data.get('interestType', 'amount')
        
        if not file_data or not principal_col or not interest_col:
            return jsonify({'error': 'Missing required data'}), 400
        
        # Convert to DataFrame
        df = pd.DataFrame(file_data)
        
        # Extract columns
        principal = pd.to_numeric(df[principal_col], errors='coerce')
        interest = pd.to_numeric(df[interest_col], errors='coerce')
        
        # Remove invalid rows
        valid_mask = (~principal.isna()) & (~interest.isna()) & (principal != 0)
        principal_clean = principal[valid_mask]
        interest_clean = interest[valid_mask]
        
        if len(principal_clean) == 0:
            return jsonify({'error': 'No valid data found'}), 400
        
        # Calculate interest rates
        if interest_type == 'amount':
            interest_rates = (interest_clean / principal_clean) * 100
        else:
            interest_rates = interest_clean
        
        # Prepare detailed breakdown
        breakdown = []
        valid_indices = valid_mask[valid_mask].index
        for i, idx in enumerate(valid_indices):
            breakdown.append({
                'row': int(idx) + 1,
                'principal': float(principal_clean.iloc[i]),
                'interest': float(interest_clean.iloc[i]),
                'rate': float(interest_rates.iloc[i])
            })
        
        # Calculate statistics
        result = {
            'average': float(interest_rates.mean()),
            'median': float(interest_rates.median()),
            'min': float(interest_rates.min()),
            'max': float(interest_rates.max()),
            'stdDev': float(interest_rates.std()),
            'count': int(len(interest_rates)),
            'breakdown': breakdown
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Error calculating interest rate: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
