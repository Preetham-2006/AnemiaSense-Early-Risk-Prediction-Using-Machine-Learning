import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\Users\jaini\Downloads\Healthcare_project\Dataset\cleaned_data.csv")

print(df.describe())

print(df.corr(numeric_only=True))

# Histogram
df.hist(figsize=(15,10))
plt.show()

# Correlation Heatmap
plt.figure(figsize=(12,8))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
plt.show()

# Class Distribution
sns.countplot(x="Anemia", data=df)
plt.show()

# Boxplot
plt.figure(figsize=(14,6))
sns.boxplot(data=df)
plt.xticks(rotation=90)
plt.show()