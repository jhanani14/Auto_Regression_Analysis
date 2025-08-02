import React from "react";
import UploadForm from "./UploadForm";

function App() {
  return (
    <div style={{ margin: "20px", fontFamily: "Roboto, sans-serif" }}>
      <h1>🧠 Auto Regression Analysis</h1>
      <p style={{ color: "#ccc" }}>
        Upload your dataset (.csv) or URL and run Linear, Ridge, or Lasso regression.
      </p>
      <UploadForm />
    </div>
  );
}

export default App;

