import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt


# ==============================
# CONFIG
# ==============================
API_URL = "https://ai-credit-scoring-platform.onrender.com/credit/score"
HISTORY_FILE = "history.csv"

st.set_page_config(
    page_title="AI Credit Scoring Platform",
    page_icon="💳",
    layout="centered"
)

# ==============================
# HEADER
# ==============================
st.markdown(
    """
    <h1 style="text-align:center;">💳 AI Credit Scoring Platform</h1>
    <h4 style="text-align:center; color:gray;">
        Alternative Credit Scoring for Micro-Finance
    </h4>
    <hr>
    """,
    unsafe_allow_html=True
)

# ==============================
# INPUTS
# ==============================
st.subheader("📥 Borrower Financial Details")

monthly_income = st.number_input("Monthly Income (₹)", min_value=0, step=1000, value=25000)
avg_upi_transactions = st.number_input("Average Monthly UPI Transactions", min_value=0, value=60)
bill_payment_ratio = st.slider("Bill Payment Ratio", 0.0, 1.0, 0.9)
income_consistency = st.slider("Income Consistency", 0.0, 1.0, 0.8)

st.markdown("---")

# ==============================
# EVALUATE
# ==============================
if st.button("🔍 Evaluate Credit", use_container_width=True):

    payload = {
        "monthly_income": monthly_income,
        "avg_upi_transactions": avg_upi_transactions,
        "bill_payment_ratio": bill_payment_ratio,
        "income_consistency": income_consistency
    }

    with st.spinner("Analyzing credit profile..."):
        response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        data = response.json()

        st.success("✅ Credit Evaluation Completed")

        # ==============================
        # SAVE HISTORY (SAFE)
        # ==============================
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "monthly_income": monthly_income,
            "upi_transactions": avg_upi_transactions,
            "bill_payment_ratio": bill_payment_ratio,
            "income_consistency": income_consistency,
            "credit_score": data["credit_score"],
            "risk_level": data["risk_level"],
            "approved": data["approved"],
            "loan_amount": data["loan_offer"]["max_amount"]
            if data["loan_offer"]["eligible"] else 0
        }

        df_new = pd.DataFrame([record])

        # 🔐 SAFE CSV HANDLING
        if os.path.exists(HISTORY_FILE) and os.path.getsize(HISTORY_FILE) > 0:
            df_old = pd.read_csv(HISTORY_FILE)
            df_all = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_all = df_new

        df_all.to_csv(HISTORY_FILE, index=False)

        # ==============================
        # DISPLAY RESULTS
        # ==============================
        col1, col2, col3 = st.columns(3)
        col1.metric("Credit Score", data["credit_score"])
        col2.metric("Risk Level", data["risk_level"])
        col3.metric("Approved", "YES ✅" if data["approved"] else "NO ❌")

        st.markdown("---")

        st.subheader("🧠 Decision Explanation")
        for reason in data["explanation"]:
            st.write("✔", reason)

        st.markdown("---")

        st.subheader("💰 Loan Offer")
        offer = data["loan_offer"]

        if offer["eligible"]:
            st.info(
                f"""
                **Max Amount:** ₹{offer['max_amount']}  
                **Interest Rate:** {offer['interest_rate']}%  
                **Tenure:** {offer['tenure_months']} months
                """
            )
        else:
            st.warning("Loan not eligible")

    else:
        st.error("🚨 API error. Is backend running?")

# ==============================
# HISTORY SECTION (SAFE)
# ==============================
st.markdown("---")
st.subheader("📜 Credit Evaluation History")

if os.path.exists(HISTORY_FILE) and os.path.getsize(HISTORY_FILE) > 0:
    history_df = pd.read_csv(HISTORY_FILE)
    st.dataframe(history_df, use_container_width=True)

    st.download_button(
        "⬇️ Download Report (CSV)",
        data=history_df.to_csv(index=False),
        file_name="credit_history_report.csv",
        mime="text/csv"
    )
else:
    st.info("No history yet. Run a credit evaluation first.")

# ==============================
# ANALYTICS DASHBOARD
# ==============================
st.markdown("---")
st.subheader("📊 Credit Analytics Dashboard")

if os.path.exists(HISTORY_FILE):
    df = pd.read_csv(HISTORY_FILE)

    if not df.empty:
        col1, col2 = st.columns(2)

        # --------------------------
        # CREDIT SCORE TREND
        # --------------------------
        with col1:
            st.markdown("#### 📈 Credit Score Trend")
            plt.figure()
            plt.plot(df["credit_score"], marker="o")
            plt.xlabel("Evaluation Count")
            plt.ylabel("Credit Score")
            st.pyplot(plt)

        # --------------------------
        # RISK LEVEL DISTRIBUTION
        # --------------------------
        with col2:
            st.markdown("#### ⚠️ Risk Level Distribution")
            risk_counts = df["risk_level"].value_counts()
            plt.figure()
            plt.pie(risk_counts, labels=risk_counts.index, autopct="%1.1f%%")
            st.pyplot(plt)

        # --------------------------
        # LOAN APPROVAL RATE
        # --------------------------
        st.markdown("#### ✅ Loan Approval Rate")
        approval_counts = df["approved"].value_counts()
        plt.figure()
        plt.bar(approval_counts.index.astype(str), approval_counts.values)
        plt.xlabel("Approved")
        plt.ylabel("Count")
        st.pyplot(plt)

    else:
        st.info("No analytics available yet.")

