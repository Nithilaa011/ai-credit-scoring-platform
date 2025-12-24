import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
import os

DATA_PATH = os.path.join("..", "data", "training_data.csv")

df = pd.read_csv(DATA_PATH)

X = df.drop("approved", axis=1)
y = df["approved"]

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, "saved_model.pkl")

print("✅ ML model trained and saved")