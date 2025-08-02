import React from "react";
import Plot from "react-plotly.js";

function RegressionPlot({ data }) {
  return (
    <Plot
      data={[
        {
          x: data.x_values,
          y: data.y_values,
          type: "scatter",
          mode: "markers",
          name: "Actual",
          marker: { color: "blue" },
        },
        {
          x: data.x_values,
          y: data.y_values,
          type: "scatter",
          mode: "lines",
          name: "Prediction",
          line: { color: "red" },
        },
      ]}
      layout={{
        width: 700,
        height: 400,
        title: `${data.model_type} Regression Plot: ${data.y_column} vs ${data.x_column}`,
        xaxis: { title: data.x_column },
        yaxis: { title: data.y_column },
      }}
    />
  );
}

export default RegressionPlot;
