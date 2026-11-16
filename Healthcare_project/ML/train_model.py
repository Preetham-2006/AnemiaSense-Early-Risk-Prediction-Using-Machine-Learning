import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from lightgbm import LGBMClassifier


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "Dataset",
    "clean_data.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "..",
    "ml_service",
    "models"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "anemia_model.pkl"
)

FEATURE_PATH = os.path.join(
    MODEL_DIR,
    "feature_names.pkl"
)


os.makedirs(MODEL_DIR, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)

print("\nColumns:")
print(list(df.columns))


# ============================================================
# CHECK TARGET
# ============================================================

if "Anemia" not in df.columns:

    raise ValueError(
        "Anemia column not found in dataset."
    )


# ============================================================
# FEATURES AND TARGET
# ============================================================

FEATURES = [
    "WardNum",
    "HB",
    "ERY",
    "HK",
    "LEUKO",
    "PLT",
    "MCV",
    "MCHC",
    "MCH",
    "RDW"
]

X = df[FEATURES].copy()
y = df["Anemia"]


print("\nTarget distribution:")
print(y.value_counts())


# ============================================================
# FEATURE NAMES
# ============================================================

feature_names = list(X.columns)

print("\nFeatures:")
print(feature_names)

print(
    "\nNumber of features:",
    len(feature_names)
)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print("\nTraining samples:")
print(len(X_train))

print("\nTesting samples:")
print(len(X_test))


# ============================================================
# LIGHTGBM
# ============================================================

print("\nTraining LightGBM...")


model = LGBMClassifier(

    objective="binary",

    n_estimators=100,

    learning_rate=0.05,

    num_leaves=15,

    max_depth=6,

    min_child_samples=50,

    subsample=0.8,

    colsample_bytree=0.8,

    reg_alpha=0.1,

    reg_lambda=0.1,

    random_state=42,

    n_jobs=-1,

    verbosity=-1

)


# ============================================================
# TRAIN
# ============================================================

model.fit(

    X_train,

    y_train

)


print("Training completed.")


# ============================================================
# PREDICTION
# ============================================================

train_pred = model.predict(X_train)

test_pred = model.predict(X_test)


# ============================================================
# METRICS
# ============================================================

train_accuracy = accuracy_score(
    y_train,
    train_pred
)

test_accuracy = accuracy_score(
    y_test,
    test_pred
)

precision = precision_score(
    y_test,
    test_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    test_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    test_pred,
    zero_division=0
)


# ============================================================
# RESULTS
# ============================================================

print("\n")
print("==========================================")
print("        LIGHTGBM MODEL RESULTS")
print("==========================================")

print(
    "Training Accuracy :",
    round(train_accuracy, 4)
)

print(
    "Testing Accuracy  :",
    round(test_accuracy, 4)
)

print(
    "Precision         :",
    round(precision, 4)
)

print(
    "Recall            :",
    round(recall, 4)
)

print(
    "F1 Score          :",
    round(f1, 4)
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        test_pred,
        zero_division=0
    )
)


print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        test_pred
    )
)


# ============================================================
# SAVE MODEL
# ============================================================

joblib.dump(
    model,
    MODEL_PATH
)

joblib.dump(
    feature_names,
    FEATURE_PATH
)


print("\n")
print("==========================================")
print("             MODEL SAVED")
print("==========================================")

print(
    "Model:",
    os.path.abspath(MODEL_PATH)
)

print(
    "Features:",
    os.path.abspath(FEATURE_PATH)
)

print("\nLightGBM training completed successfully.")