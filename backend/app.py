from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from model import run_regression_models
from report_generator import generate_pdf_report
from db_config import get_connection

import pandas as pd
import json
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app)

@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files.get("file")
        url = request.form.get("url")
        name = request.form.get("name") or "Unnamed Dataset"

        # Read the CSV
        if file:
            df = pd.read_csv(file)
        elif url:
            df = pd.read_csv(url)
        else:
            return jsonify({"error": "No file or URL provided"}), 400

        # Convert DataFrame to JSON string before saving
        json_str = json.dumps(df.to_dict(orient="records"))

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO datasets (name, data) VALUES (%s, %s) RETURNING id",
            (name, json_str)
        )
        dataset_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Uploaded", "dataset_id": dataset_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/regress", methods=["POST"])
def regress():
    try:
        dataset_id = request.json.get("dataset_id")
        model_type = request.json.get("model_type", "linear")

        # Fetch JSON from DB
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT data FROM datasets WHERE id = %s", (dataset_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return jsonify({"error": "Dataset not found"}), 404

        data = row[0]

        # Safely convert JSON string to DataFrame
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame(json.loads(data))

        results, residual_plot, reg_plot = run_regression_models(df, model_type)

        pdf_filename = f"report_{dataset_id}.pdf"
        generate_pdf_report(results, reg_plot, residual_plot, pdf_filename)

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/report/<int:dataset_id>", methods=["GET"])
def download_report(dataset_id):
    pdf_path = f"report_{dataset_id}.pdf"
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    else:
        return jsonify({"error": "Report not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
