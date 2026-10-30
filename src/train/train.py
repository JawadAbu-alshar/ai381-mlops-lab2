
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Locate the project root regardless of where the script is run.
ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "churn_v2.csv"
MODEL_PATH = ROOT / "model.joblib"


def main():
    # 1. Load the dataset
    df = pd.read_csv(DATA_PATH)

    # 2. Select features and target
    numeric = ["tenure_months", "monthly_fee", "support_calls"]
    categorical = ["contract", "internet_service"]

    X = df[numeric + categorical]
    y = df["churn"]

    # 3. Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # 4. Create preprocessing and classification pipeline
    model = Pipeline([
        ("prep", ColumnTransformer([
            ("num", StandardScaler(), numeric),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ])),
        ("clf", LogisticRegression(max_iter=1000)),
    ])

    # 5. Train the model
    model.fit(X_train, y_train)

    # 6. Evaluate the model
    proba = model.predict_proba(X_test)[:, 1]

    print("F1 :", round(f1_score(y_test, proba > 0.5), 3))
    print("AUC:", round(roc_auc_score(y_test, proba), 3))

    # 7. Save the trained model
    joblib.dump(model, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
