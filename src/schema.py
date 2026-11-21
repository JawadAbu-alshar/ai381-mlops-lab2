FEATURES = ["tenure_months", "monthly_fee", "support_calls", "contract", "internet_service"]
NUMERIC = ["tenure_months", "monthly_fee", "support_calls"]
CATEGORICAL = ["contract", "internet_service"]
TARGET = "churn"


def validate(df):
    required = FEATURES + [TARGET]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df
