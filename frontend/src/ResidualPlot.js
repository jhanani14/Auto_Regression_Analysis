import React from "react";
import Plot from "react-plotly.js";

function ResidualPlot({ y, y_pred }) {
  const residuals = y.map((val, i) => val - y_pred[i]);

  return (
    <Plot
      data={[
        {
          x: y_pred,
          y: residuals,
          mode: "markers",
          type: "scatter",
          name: "Residuals",
          marker: { color: "purple" },
        },
      ]}
      layout={{
        width: 700,
        height: 400,
        title: "Residual Plot",
        xaxis: { title: "Predicted" },
        yaxis: { title: "Residuals (y - ŷ)" },
      }}
    />
  );
}

export default ResidualPlot;
