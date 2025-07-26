function ModelExplanation() {
  return (
    <div style={{ marginTop: "30px" }}>
      <h2>🧠 Model Explanation</h2>
      <p><strong>Linear Regression:</strong> Best-fit line through the data.</p>
      <p><strong>Ridge:</strong> Shrinks coefficients to reduce overfitting (L2 regularization).</p>
      <p><strong>Lasso:</strong> Shrinks and removes unnecessary features (L1 regularization).</p>
      <p><strong>R² Score:</strong> Shows model accuracy (closer to 1 is better).</p>
    </div>
  );
}

export default ModelExplanation;
