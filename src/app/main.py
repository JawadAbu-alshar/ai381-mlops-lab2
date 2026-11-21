import json
import os
from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "model.joblib"
METADATA_PATH = ROOT / "metadata.json"

model = joblib.load(MODEL_PATH)
metadata = json.loads(METADATA_PATH.read_text()) if METADATA_PATH.exists() else {}

app = FastAPI(title="AI381 Lab 3 Churn API")


class CustomerInput(BaseModel):
    tenure_months: int = Field(ge=0)
    monthly_fee: float = Field(ge=0)
    contract: Literal["month-to-month", "one-year", "two-year"]
    internet_service: Literal["fiber", "none", "dsl"]
    support_calls: int = Field(ge=0)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_version": os.getenv("GIT_SHA", metadata.get("model_version", "unknown"))[:7],
        "mlflow_run_id": metadata.get("mlflow_run_id", "unknown"),
    }


@app.post("/predict")
def predict(customer: CustomerInput):
    X = pd.DataFrame([customer.model_dump()])
    probability = float(model.predict_proba(X)[0, 1])
    return {"churn_probability": round(probability, 3)}