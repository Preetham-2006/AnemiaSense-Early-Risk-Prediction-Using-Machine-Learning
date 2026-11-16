import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "ml_service", "models", "anemia_model.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "..", "ml_service", "models", "feature_names.pkl")

model = joblib.load(MODEL_PATH)
feature_names = list(joblib.load(FEATURE_PATH))

print("\n======================================")
print("LIGHTGBM MODEL LOADED")
print("======================================")
print("Model:", type(model).__name__)
print("Features:", feature_names)
print("Number of features:", len(feature_names))


def predict_anemia(data):
    missing = [feature for feature in feature_names if feature not in data]
    if missing:
        raise ValueError(f"Model features missing: {missing}")

    df = pd.DataFrame([[data[feature] for feature in feature_names]], columns=feature_names)
    df = df.apply(pd.to_numeric, errors="raise")

    if df.isnull().any().any():
        raise ValueError("CBC values contain invalid or missing numbers.")

    print("Data sent to LightGBM:")
    print(df.to_dict(orient="records")[0])

    prediction = int(model.predict(df)[0])
    probability = None
    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(df)[0][1])

    return {"prediction": prediction, "probability": probability}
