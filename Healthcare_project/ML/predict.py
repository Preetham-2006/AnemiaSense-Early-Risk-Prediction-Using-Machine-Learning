import pandas as pd
import joblib

# Load model
model = joblib.load(
    r"C:\Users\jaini\Downloads\Healthcare_project_FIXED\Healthcare_project\ml_service\models\anemia_model.pkl"
)

# Load feature names
feature_names = joblib.load(
    r"C:\Users\jaini\Downloads\Healthcare_project_FIXED\Healthcare_project\ml_service\models\feature_names.pkl"
)

print("Enter patient details:")

values = []

for feature in feature_names:
    value = float(input(f"{feature}: "))
    values.append(value)

# Create input DataFrame
patient_data = pd.DataFrame(
    [values],
    columns=feature_names
)

# Predict
prediction = model.predict(patient_data)[0]

# Probability
probability = model.predict_proba(patient_data)[0]

print("\n========== PREDICTION ==========")

if prediction == 1:
    print("Prediction: Anemia Detected")
    print("Probability:", round(probability[1] * 100, 2), "%")
else:
    print("Prediction: No Anemia Detected")
    print("Probability:", round(probability[0] * 100, 2), "%")