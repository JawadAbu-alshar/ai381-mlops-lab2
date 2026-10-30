
from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Project root and saved model path
ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "model.joblib"

# Load the trained model
model = joblib.load(MODEL_PATH)

# Create the FastAPI application
app = FastAPI(title="AI381 Lab 2 Churn API")


# Request schema with Pydantic validation
class CustomerInput(BaseModel):
    tenure_months: int = Field(ge=0)
    monthly_fee: float = Field(ge=0)
    contract: Literal["month-to-month", "one-year", "two-year"]
    internet_service: Literal["fiber", "none", "dsl"]
    support_calls: int = Field(ge=0)


# Health endpoint
@app.get("/health")
def health():
    return {"status": "ok"}


# Prediction endpoint
@app.post("/predict")
def predict(customer: CustomerInput):
    # Convert validated input into a DataFrame
    X = pd.DataFrame([customer.model_dump()])

    # Predict churn probability
    probability = float(model.predict_proba(X)[0, 1])

    return {"churn_probability": round(probability, 3)}
