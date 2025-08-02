import React, { useState } from "react";
import axios from "axios";
import RegressionPlot from "./RegressionPlot";
import ResidualPlot from "./ResidualPlot";
import ModelExplanation from "./ModelExplanation";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [datasetUrl, setDatasetUrl] = useState("");
  const [modelType, setModelType] = useState("linear");
  const [result, setResult] = useState(null);
  const [datasetId, setDatasetId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setDatasetUrl("");
    setResult(null);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      if (file) formData.append("file", file);
      if (datasetUrl) formData.append("url", datasetUrl);
      formData.append("name", "Uploaded Dataset");

      const uploadRes = await axios.post("http://localhost:5000/upload", formData);
      const id = uploadRes.data.dataset_id;
      setDatasetId(id);

      const regressRes = await axios.post("http://localhost:5000/regress", {
        dataset_id: id,
        model_type: modelType,
      });

      setResult(regressRes.data);
    } catch (err) {
      const msg = err.response?.data?.error || "Upload or regression failed.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = async () => {
    try {
      const res = await axios.get(`http://localhost:5000/report/${datasetId}`, {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "regression_report.pdf");
      document.body.appendChild(link);
      link.click();
    } catch {
      alert("Failed to download PDF.");
    }
  };

  return (
    <div>
      <h2>📂 Upload CSV or Dataset URL</h2>
      <form onSubmit={handleSubmit}>
        <label><strong>Model Type:</strong></label>
        <select value={modelType} onChange={(e) => setModelType(e.target.value)}>
          <option value="linear">Linear</option>
          <option value="ridge">Ridge</option>
          <option value="lasso">Lasso</option>
        </select>

        <br /><br />
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <br /><br />
        <input
          type="text"
          value={datasetUrl}
          onChange={(e) => setDatasetUrl(e.target.value)}
          placeholder="Or paste dataset URL (.csv)"
          style={{ width: "100%" }}
        />
        <br /><br />
        <button type="submit" disabled={loading}>
          {loading ? "Processing..." : "Run Regression"}
        </button>
      </form>

      <br />
      {error && <p style={{ color: "red" }}>{error}</p>}

      {result ? (
        <div>
          <h3>📈 Results</h3>
          <p><strong>Model:</strong> {result.model_type}</p>
          <p><strong>Y Column:</strong> {result.y_column || "N/A"}</p>
          <p><strong>X Columns:</strong> {Array.isArray(result.x_columns) ? result.x_columns.join(", ") : "N/A"}</p>
          <p><strong>Intercept:</strong> {result.intercept !== undefined ? result.intercept.toFixed(3) : "N/A"}</p>
          <p><strong>R² Score:</strong> {result.r2 !== undefined ? result.r2.toFixed(3) : "N/A"}</p>

          <p><strong>Coefficients:</strong></p>
          <ul>
            {result.coef ? (
              Object.entries(result.coef).map(([key, val]) => (
                <li key={key}>{key}: {val !== undefined ? val.toFixed(3) : "N/A"}</li>
              ))
            ) : (
              <li>No coefficients found</li>
            )}
          </ul>

          <button onClick={downloadPDF}>📥 Download PDF Report</button>

          <RegressionPlot
            data={{
              x_values: result.y_values || [],
              y_values: result.y_pred || [],
              x_column: "Actual Y",
              y_column: "Predicted Y",
              model_type: result.model_type
            }}
          />

          <ResidualPlot y={result.y_values || []} y_pred={result.y_pred || []} />
        </div>
      ) : (
        !loading && <p>No results yet. Please upload and run.</p>
      )}

      <ModelExplanation />
    </div>
  );
}

export default UploadForm;
