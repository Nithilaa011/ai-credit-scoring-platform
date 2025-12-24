def loan_decision_engine(credit_score: int):
    if credit_score >= 750:
        return {
            "eligible": True,
            "max_amount": 150000,
            "interest_rate": 12,
            "tenure_months": 24
        }

    elif credit_score >= 650:
        return {
            "eligible": True,
            "max_amount": 80000,
            "interest_rate": 16,
            "tenure_months": 18
        }

    else:
        return {
            "eligible": False,
            "max_amount": 0,
            "interest_rate": None,
            "tenure_months": None
        }
