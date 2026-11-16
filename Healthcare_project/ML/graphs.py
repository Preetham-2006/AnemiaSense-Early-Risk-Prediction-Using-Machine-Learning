import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    roc_curve,
    precision_recall_curve
)
from lightgbm import LGBMClassifier


# ============================================================
# ANEMIASENSE - LIGHTGBM METRICS AND 8 GRAPHS
# ============================================================
# This script:
# 1. Loads cleaned_data.csv
# 2. Excludes HB because it directly leaks the Anemia target
# 3. Trains LightGBM
# 4. Calculates Accuracy, Precision, Recall, F1 and ROC-AUC
# 5. Generates 8 graphs
#
# Change DATA_PATH if your CSV is in another location.
# ============================================================


DATA_PATH = r"C:\Users\jaini\Downloads\Healthcare_project\Dataset\cleaned_data.csv"

OUTPUT_DIR = "anemia_graphs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 1. LOAD DATA
# ============================================================

print("=" * 65)
print("ANEMIASENSE - LIGHTGBM MODEL EVALUATION")
print("=" * 65)

df = pd.read_csv(DATA_PATH)

print("\nDataset shape:", df.shape)

if "Anemia" not in df.columns:
    raise ValueError("The 'Anemia' target column was not found.")


# Remove duplicates
df = df.drop_duplicates().reset_index(drop=True)

# Remove rows with missing target
df = df.dropna(subset=["Anemia"]).reset_index(drop=True)


# ============================================================
# 2. FEATURES
# ============================================================
# HB is excluded because it is the leakage feature identified
# in this dataset.
#
# Use the CBC features available in the dataset.
# The three features below are the corrected model inputs.
# ============================================================

FEATURES = ["ERY", "MCHC", "RDW","PLT"]

missing_features = [
    col for col in FEATURES
    if col not in df.columns
]

if missing_features:
    raise ValueError(
        "Missing feature(s): " + str(missing_features)
    )


X = df[FEATURES].copy()
y = df["Anemia"].astype(int)


# Make sure features are numeric
for col in FEATURES:
    X[col] = pd.to_numeric(X[col], errors="coerce")

valid_rows = X.notna().all(axis=1)

X = X.loc[valid_rows].reset_index(drop=True)
y = y.loc[valid_rows].reset_index(drop=True)


print("\nFeatures used:")
print(FEATURES)

print("\nHB is NOT used as an input feature.")


# ============================================================
# 3. CLASS DISTRIBUTION
# ============================================================

print("\nClass distribution:")
print(y.value_counts().sort_index())


# ============================================================
# 4. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ============================================================
# 5. LIGHTGBM
# ============================================================

model = LGBMClassifier(
    n_estimators=100,
    learning_rate=0.03,
    num_leaves=8,
    max_depth=3,
    min_child_samples=100,
    reg_alpha=1.0,
    reg_lambda=2.0,
    random_state=42,
    n_jobs=-1,
    verbosity=-1
)


print("\nTraining LightGBM...")

model.fit(X_train, y_train)


# ============================================================
# 6. PREDICTIONS
# ============================================================

train_pred = model.predict(X_train)
test_pred = model.predict(X_test)

test_probability = model.predict_proba(X_test)[:, 1]


# ============================================================
# 7. METRICS
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

roc_auc = roc_auc_score(
    y_test,
    test_probability
)


print("\n")
print("=" * 65)
print("LIGHTGBM MODEL RESULTS")
print("=" * 65)

print(f"Training Accuracy : {train_accuracy:.4f}")
print(f"Testing Accuracy  : {test_accuracy:.4f}")
print(f"Precision         : {precision:.4f}")
print(f"Recall            : {recall:.4f}")
print(f"F1 Score          : {f1:.4f}")
print(f"ROC-AUC           : {roc_auc:.4f}")


# ============================================================
# 8. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test,
    test_pred
)

print("\nConfusion Matrix:")
print(cm)


# ============================================================
# GRAPH 1 - ACTUAL VS PREDICTED
# ============================================================

sample_size = min(1000, len(y_test))

actual = y_test.iloc[:sample_size].to_numpy()
predicted = test_pred[:sample_size]

plt.figure(figsize=(12, 5))

plt.plot(
    range(sample_size),
    actual,
    label="Actual",
    linewidth=1
)

plt.plot(
    range(sample_size),
    predicted,
    label="Predicted",
    linewidth=1
)

plt.xlabel("Test Sample")
plt.ylabel("Anemia Class")

plt.title(
    "Actual vs Predicted - LightGBM"
)

plt.yticks(
    [0, 1],
    ["No Anemia", "Anemia"]
)

plt.legend()

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "01_actual_vs_predicted.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# GRAPH 2 - CONFUSION MATRIX
# ============================================================

plt.figure(figsize=(7, 6))

plt.imshow(cm)

plt.title(
    "Confusion Matrix - LightGBM"
)

plt.xlabel("Predicted")

plt.ylabel("Actual")

plt.xticks(
    [0, 1],
    ["No Anemia", "Anemia"]
)

plt.yticks(
    [0, 1],
    ["No Anemia", "Anemia"]
)

for i in range(2):
    for j in range(2):
        plt.text(
            j,
            i,
            f"{cm[i, j]:,}",
            ha="center",
            va="center"
        )

plt.colorbar(
    label="Number of Samples"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "02_confusion_matrix.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# GRAPH 3 - TRAINING VS TESTING ACCURACY
# ============================================================

plt.figure(figsize=(8, 5))

values = [
    train_accuracy * 100,
    test_accuracy * 100
]

bars = plt.bar(
    ["Training", "Testing"],
    values
)

plt.ylabel("Accuracy (%)")

plt.title(
    "Training vs Testing Accuracy - LightGBM"
)

plt.ylim(0, 100)

for bar, value in zip(bars, values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 1,
        f"{value:.2f}%",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "03_training_vs_testing_accuracy.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# GRAPH 4 - CLASS DISTRIBUTION
# ============================================================

class_counts = y.value_counts().sort_index()

plt.figure(figsize=(8, 5))

bars = plt.bar(
    ["No Anemia", "Anemia"],
    class_counts.values
)

plt.ylabel("Number of Samples")

plt.title(
    "Anemia Dataset Class Distribution"
)

for bar, value in zip(bars, class_counts.values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + max(class_counts.values) * 0.01,
        f"{value:,}",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "04_class_distribution.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# GRAPH 5 - LIGHTGBM FEATURE IMPORTANCE
# ============================================================

importance = pd.DataFrame({
    "Feature": FEATURES,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    "Importance",
    ascending=True
)

plt.figure(figsize=(8, 5))

plt.barh(
    importance["Feature"],
    importance["Importance"]
)

plt.xlabel("Importance")

plt.ylabel("Feature")

plt.title(
    "LightGBM Feature Importance"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "05_lightgbm_feature_importance.png"
    ),
    dpi=300
)

plt.close()

importance.sort_values(
    "Importance",
    ascending=False
).to_csv(
    os.path.join(
        OUTPUT_DIR,
        "feature_importance.csv"
    ),
    index=False
)


# ============================================================
# GRAPH 6 - ROC CURVE
# ============================================================

fpr, tpr, _ = roc_curve(
    y_test,
    test_probability
)

plt.figure(figsize=(8, 6))

plt.plot(
    fpr,
    tpr,
    linewidth=2,
    label=f"LightGBM (AUC = {roc_auc:.4f})"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    label="Random Classifier"
)

plt.xlabel("False Positive Rate")

plt.ylabel("True Positive Rate")

plt.title(
    "ROC Curve - LightGBM"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "06_roc_curve.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# GRAPH 7 - PRECISION RECALL CURVE
# ============================================================

precision_values, recall_values, _ = (
    precision_recall_curve(
        y_test,
        test_probability
    )
)

plt.figure(figsize=(8, 6))

plt.plot(
    recall_values,
    precision_values,
    linewidth=2
)

plt.xlabel("Recall")

plt.ylabel("Precision")

plt.title(
    "Precision-Recall Curve - LightGBM"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "07_precision_recall_curve.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# GRAPH 8 - PREDICTION PROBABILITY DISTRIBUTION
# ============================================================

plt.figure(figsize=(9, 6))

plt.hist(
    test_probability[y_test.to_numpy() == 0],
    bins=30,
    alpha=0.6,
    label="No Anemia"
)

plt.hist(
    test_probability[y_test.to_numpy() == 1],
    bins=30,
    alpha=0.6,
    label="Anemia"
)

plt.xlabel(
    "Predicted Probability of Anemia"
)

plt.ylabel(
    "Number of Samples"
)

plt.title(
    "LightGBM Prediction Probability Distribution"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "08_prediction_probability_distribution.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# 9. SAVE METRICS
# ============================================================

metrics_df = pd.DataFrame([{
    "Model": "LightGBM",
    "Training Accuracy": train_accuracy,
    "Testing Accuracy": test_accuracy,
    "Precision": precision,
    "Recall": recall,
    "F1 Score": f1,
    "ROC AUC": roc_auc
}])

metrics_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "lightgbm_metrics.csv"
    ),
    index=False
)


# ============================================================
# 10. SAVE TEST PREDICTIONS
# ============================================================

prediction_df = X_test.copy()

prediction_df["Actual"] = y_test.to_numpy()
prediction_df["Predicted"] = test_pred
prediction_df["Prediction Probability"] = test_probability

prediction_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "test_predictions.csv"
    ),
    index=False
)


# ============================================================
# COMPLETE
# ============================================================

print("\n")
print("=" * 65)
print("ALL GRAPHS GENERATED")
print("=" * 65)

print("\nOutput folder:")
print(os.path.abspath(OUTPUT_DIR))

print("\nGenerated files:")

for filename in sorted(os.listdir(OUTPUT_DIR)):
    print(" -", filename)

print("\nDone.")
