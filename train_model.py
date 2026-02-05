import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

if not os.path.exists('model'):
    os.makedirs('model')

FEATURES = [
    "age","gender","height","weight",
    "ap_hi","ap_lo","cholesterol",
    "gluc","smoke","alco","active"
]

df = pd.read_csv("backend/cardio_dataset.csv", sep=";")

X = df[FEATURES]
y = df["cardio"]

xtrain, xtest, ytrain, ytest = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
xtrain_scaled = scaler.fit_transform(xtrain)

# ⚡ FAST probability model
model = LogisticRegression(max_iter=1000)
model.fit(xtrain_scaled, ytrain)

joblib.dump(model, "model/logistic_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")

print("✅ Logistic Regression trained FAST with probability")
