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

    const formData = new FormData();
    if (file) formData.append("file", file);
    if (datasetUrl) formData.append("dataset_url", datasetUrl);
    formData.append("model_type", modelType);

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await axios.post("http://localhost:5000/api/upload", formData);
      setResult(res.data);
    } catch (err) {
      const msg = err.response?.data?.error || "Upload failed.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = async () => {
    const res = await axios.get("http://localhost:5000/api/report", { responseType: "blob" });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "regression_report.pdf");
    document.body.appendChild(link);
    link.click();
  };

  return (
    <div>
      <h2>Upload CSV or Dataset URL</h2>
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

      {result && (
        <div>
          <h3>Results</h3>
          <p><strong>Model:</strong> {result.model_type}</p>
          <p><strong>Y Column:</strong> {result.y_column}</p>
          <p><strong>X Column(s):</strong> {Array.isArray(result.x_columns) ? result.x_columns.join(", ") : result.x_columns}</p>
          <p><strong>Intercept:</strong> {result.intercept.toFixed(3)}</p>
          <p><strong>R² Score:</strong> {result.r2.toFixed(3)}</p>

          <p><strong>Coefficients:</strong></p>
          <ul>
            {Object.entries(result.coef).map(([key, val]) => (
              <li key={key}>{key}: {val.toFixed(3)}</li>
            ))}
          </ul>

          <button onClick={downloadPDF}>📥 Download PDF Report</button>

          <RegressionPlot
            data={{
              x_values: result.y_values,
              y_values: result.y_pred,
              y_pred: result.y_values,
              x_column: "Actual Y",
              y_column: "Predicted Y"
            }}
          />

          <ResidualPlot y={result.y_values} y_pred={result.y_pred} />
        </div>
      )}

      <ModelExplanation />
    </div>
  );
}

export default UploadForm;
