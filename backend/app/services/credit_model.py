import joblib
import os
from app.services.loan_logic import loan_decision_engine

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "saved_model.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_credit_score(features: dict):
    X = [[
        features["monthly_income"],
        features["avg_upi_transactions"],
        features["bill_payment_ratio"],
        features["income_consistency"]
    ]]

    probability = model.predict_proba(X)[0][1]
    credit_score = int(300 + probability * 600)

    risk_level = (
        "LOW" if credit_score >= 700 else
        "MEDIUM" if credit_score >= 600 else
        "HIGH"
    )

    approved = credit_score >= 650

    # 🧠 Explainability
    explanation = []

    if features["monthly_income"] >= 20000:
        explanation.append("Stable monthly income")

    if features["bill_payment_ratio"] >= 0.8:
        explanation.append("Good bill payment history")

    if features["income_consistency"] >= 0.7:
        explanation.append("Consistent income pattern")

    if features["avg_upi_transactions"] >= 50:
        explanation.append("High digital transaction activity")

    if not explanation:
        explanation.append("Limited financial activity observed")

    # 💰 Loan logic
    loan_offer = loan_decision_engine(credit_score)

    return {
        "credit_score": credit_score,
        "risk_level": risk_level,
        "approved": approved,
        "explanation": explanation,
        "loan_offer": loan_offer
    }
