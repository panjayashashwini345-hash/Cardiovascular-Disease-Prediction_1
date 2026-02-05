from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

# Load the Logistic Regression model you just trained
try:
    model = joblib.load("model/logistic_model.pkl")
    scaler = joblib.load("model/scaler.pkl")
    print("✅ Model/Scaler loaded successfully")
except Exception as e:
    print("❌ Error loading model files:", e)

FEATURES = ["age","gender","height","weight","ap_hi","ap_lo","cholesterol","gluc","smoke","alco","active"]

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    try:
        # CONVERSION: The dataset uses days, so we multiply years by 365.25
        data['age'] = float(data['age']) * 365.25

        # Feature ordering
        values = [float(data[f]) for f in FEATURES]
        scaled_values = scaler.transform([values])

        # Get probability (0.0 to 1.0)
        probability = model.predict_proba(scaled_values)[0][1]
        percentage = round(probability * 100, 2)

        # Labels for the UI
        risk = "High" if percentage >= 50 else "Low"

        return jsonify({
            "percentage": percentage,
            "risk": risk
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)