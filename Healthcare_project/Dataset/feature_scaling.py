import pandas as pd
import joblib

from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv(r"C:\Users\jaini\Downloads\Healthcare_project\Dataset\cleaned_data.csv")

# Features and target
X = df.drop("Anemia", axis=1)
y = df["Anemia"]

# Remove identifier columns if present
drop_cols = ["SampleNum", "PatientNum", "Timestamp"]

for col in drop_cols:
    if col in X.columns:
        X = X.drop(columns=col)

# Convert Timestamp only if you really want to keep it
# Example:
# X["Timestamp"] = pd.to_datetime(df["Timestamp"])
# X["Year"] = X["Timestamp"].dt.year
# X["Month"] = X["Timestamp"].dt.month
# X["Day"] = X["Timestamp"].dt.day
# X = X.drop("Timestamp", axis=1)

# Encode only categorical columns
categorical_columns = X.select_dtypes(include="object").columns

if len(categorical_columns) > 0:
    X = pd.get_dummies(X, columns=categorical_columns, drop_first=True)

# Scale
scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

processed = pd.DataFrame(X_scaled, columns=X.columns)

processed["Anemia"] = y.values

processed.to_csv("processed_data.csv", index=False)

joblib.dump(scaler, "../saved_models/scaler.pkl")

joblib.dump(list(X.columns), "../saved_models/feature_names.pkl")

print("Feature scaling completed successfully.")