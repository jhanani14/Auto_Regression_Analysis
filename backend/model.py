import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import r2_score
import sqlite3, datetime

DB_PATH = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS regression_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_type TEXT,
            coef TEXT,
            intercept REAL,
            r2 REAL,
            created_at TEXT,
            dataset_name TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_results(model_type, coef, intercept, r2, dataset_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO regression_results (model_type, coef, intercept, r2, created_at, dataset_name)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (model_type, str(coef), intercept, r2, datetime.datetime.now().isoformat(), dataset_name))
    conn.commit()
    conn.close()

def run_regression(df, x_cols, y_col, model_type="linear", dataset_name="uploaded_data"):
    df = df[x_cols + [y_col]].dropna()
    X = df[x_cols].values
    y = df[y_col].values

    if model_type == "ridge":
        model = Ridge(alpha=1.0)
    elif model_type == "lasso":
        model = Lasso(alpha=0.1)
    else:
        model = LinearRegression()

    model.fit(X, y)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)

    coef = dict(zip(x_cols, model.coef_))
    intercept = model.intercept_

    save_results(model_type, coef, intercept, r2, dataset_name)

    return coef, intercept, r2, x_cols, y_col, y.tolist(), y_pred.tolist()

def compare_models(df, x_cols, y_col):
    df = df[x_cols + [y_col]].dropna()
    X = df[x_cols].values
    y = df[y_col].values

    models = {
        "linear": LinearRegression(),
        "ridge": Ridge(alpha=1.0),
        "lasso": Lasso(alpha=0.1)
    }

    results = {}

    for name, model in models.items():
        model.fit(X, y)
        y_pred = model.predict(X)
        r2 = r2_score(y, y_pred)
        results[name] = {
            "coef": dict(zip(x_cols, model.coef_)),
            "intercept": model.intercept_,
            "r2": r2,
        }

    return results
