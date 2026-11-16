import pandas as pd
import time

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier

from lightgbm import LGBMClassifier


# Load dataset
df = pd.read_csv(
    r"C:\Users\jaini\Downloads\AnemiaSense_LightGBM_FIXED\Healthcare_project\Dataset\clean_data.csv"
)

# Features and target
X = df.drop("Anemia", axis=1)
y = df["Anemia"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Models
models = {

    "Logistic Regression":
        LogisticRegression(max_iter=1000),

    "Decision Tree":
        DecisionTreeClassifier(
            random_state=42
        ),

    "Gradient Boosting":
        GradientBoostingClassifier(
            random_state=42
        ),

    "AdaBoost":
        AdaBoostClassifier(
            random_state=42
        ),


        

    "LightGBM":
        LGBMClassifier(
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
}


print("\n========== MODEL COMPARISON ==========\n")

results = []

for name, model in models.items():

    start = time.time()

    model.fit(X_train, y_train)

    training_time = time.time() - start

    prediction = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        prediction
    )

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Training Time": training_time
    })

    print(
        f"{name}: "
        f"Accuracy = {accuracy:.4f}, "
        f"Training Time = {training_time:.2f}s"
    )


print("\n========== SUMMARY ==========\n")

results_df = pd.DataFrame(results)

print(results_df.to_string(index=False))