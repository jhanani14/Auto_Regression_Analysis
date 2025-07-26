from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import requests
from io import StringIO
from model import run_regression, init_db
from report_generator import generate_pdf

app = Flask(__name__)
CORS(app)

# Initialize database
init_db()

@app.route('/api/upload', methods=['POST'])
def upload():
    model_type = request.form.get('model_type', 'linear').lower()
    url = request.form.get('dataset_url')

    df = None
    filename = "uploaded_data.csv"

    # Get file or URL
    if 'file' in request.files:
        file = request.files['file']
        filename = file.filename
        if filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            return jsonify({"error": "Only CSV files are supported"}), 400
    elif url:
        try:
            response = requests.get(url)
            df = pd.read_csv(StringIO(response.text))
            filename = url.split("/")[-1]
        except:
            return jsonify({"error": "Failed to load URL"}), 400
    else:
        return jsonify({"error": "No dataset provided"}), 400

    # ✅ Auto-select numeric columns
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if len(numeric_cols) < 2:
        return jsonify({"error": "Need at least 2 numeric columns"}), 400

    x_cols = numeric_cols[:-1]  # All but last
    y_col = numeric_cols[-1]   # Last column

    try:
        coef, intercept, r2, x_cols, y_col, y_vals, y_pred = run_regression(
            df, x_cols, y_col, model_type, filename
        )
        generate_pdf(coef, intercept, r2, model_type)  # PDF saved

        return jsonify({
            "coef": coef,
            "intercept": intercept,
            "r2": r2,
            "x_columns": x_cols,
            "y_column": y_col,
            "y_values": y_vals,
            "y_pred": y_pred,
            "model_type": model_type
        })
    except Exception as e:
        return jsonify({"error": f"Regression failed: {str(e)}"}), 500

@app.route('/api/report', methods=['GET'])
def download_report():
    try:
        return send_file("report.pdf", as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"Download failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
