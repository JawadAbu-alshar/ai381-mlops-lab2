
from fastapi.testclient import TestClient

from src.app.main import app, model

# Create a test client for the FastAPI application
client = TestClient(app)


# Test 1: Check the health endpoint
def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Test 2: Check that the trained model loads correctly
def test_model_loads():
    assert model is not None
    assert hasattr(model, "predict_proba")
# Test 3: Reject requests with missing required fields
def test_input_schema():
    customer = {
        "tenure_months": 12,
        "contract": "month-to-month",
        "internet_service": "fiber",
        "support_calls": 3,
    }

    response = client.post("/predict", json=customer)

    assert response.status_code == 422
    # Test 4: Reject negative tenure (edge case)
def test_negative_tenure():
    customer = {
        "tenure_months": -5,
        "monthly_fee": 75.0,
        "contract": "month-to-month",
        "internet_service": "fiber",
        "support_calls": 3,
    }

    response = client.post("/predict", json=customer)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == [
        "body", "tenure_months"
    ]
    # Test 5: Same input should produce the same prediction
def test_deterministic_prediction():
    customer = {
        "tenure_months": 12,
        "monthly_fee": 75.0,
        "contract": "month-to-month",
        "internet_service": "fiber",
        "support_calls": 3,
    }

    response1 = client.post("/predict", json=customer)
    response2 = client.post("/predict", json=customer)

    assert response1.status_code == 200
    assert response2.status_code == 200

    assert response1.json() == response2.json()