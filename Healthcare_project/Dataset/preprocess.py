import pandas as pd
import numpy as np

# Load Dataset
df = pd.read_csv(r"C:\Users\jaini\Downloads\KL_dataset.csv")

print(df.head())

print(df.shape)

print(df.info())

# Missing Values
print(df.isnull().sum())

# Fill Numeric Missing Values
numeric_columns = df.select_dtypes(include=np.number).columns

for col in numeric_columns:
    df[col].fillna(df[col].median(), inplace=True)

# Fill Categorical Missing Values
categorical_columns = df.select_dtypes(include="object").columns

for col in categorical_columns:
    df[col].fillna(df[col].mode()[0], inplace=True)

# Remove Duplicate Records
df.drop_duplicates(inplace=True)

# Drop Unnecessary Columns
drop_columns = ["SampleNum", "PatientNum", "Timestamp"]

for col in drop_columns:
    if col in df.columns:
        df.drop(col, axis=1, inplace=True)

# Create Target Variable
# NOTE:
# Replace with WHO criteria if gender data becomes available.

df["Anemia"] = df["HB"].apply(lambda x: 1 if x < 12 else 0)

print(df["Anemia"].value_counts())

# Save Cleaned Dataset
df.to_csv("../dataset/cleaned_data.csv", index=False)

print("Cleaning Completed Successfully")