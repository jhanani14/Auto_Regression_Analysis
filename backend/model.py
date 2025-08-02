import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def run_regression_models(df, model_type="linear"):
    df = df.dropna()
    y = df.iloc[:, -1]
    X = df.iloc[:, :-1]

    if model_type == "linear":
        model = LinearRegression()
    elif model_type == "ridge":
        model = Ridge(alpha=1.0)
    elif model_type == "lasso":
        model = Lasso(alpha=0.1)
    else:
        raise ValueError("Invalid model type")

    model.fit(X, y)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)

    # Regression Plot
    fig1, ax1 = plt.subplots()
    ax1.scatter(y, y_pred, color="blue")
    ax1.plot(y, y, color="red", linestyle="--")
    ax1.set_xlabel("Actual")
    ax1.set_ylabel("Predicted")
    ax1.set_title("Regression Plot")
    buf1 = BytesIO()
    fig1.savefig(buf1, format="png")
    buf1.seek(0)

    # Residual Plot
    residuals = y - y_pred
    fig2, ax2 = plt.subplots()
    ax2.scatter(y_pred, residuals, color="purple")
    ax2.axhline(y=0, color="red", linestyle="--")
    ax2.set_xlabel("Predicted")
    ax2.set_ylabel("Residuals")
    ax2.set_title("Residual Plot")
    buf2 = BytesIO()
    fig2.savefig(buf2, format="png")
    buf2.seek(0)

    results = {
        "model_type": model_type,
        "x_columns": list(X.columns),
        "y_column": y.name,
        "intercept": model.intercept_,
        "r2": r2,
        "coef": dict(zip(X.columns, model.coef_)),
        "y_values": list(y),
        "y_pred": list(y_pred),
    }

    return results, buf2, buf1
