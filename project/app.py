import streamlit as st
from models.loan_case import LoanCase
from core.decision_engine import evaluate
from utils.db import init_db

init_db()

st.title("Explainable Loan Decision Engine")

with st.form("loan_form"):
    income = st.number_input("Monthly Income", min_value=0.0)
    commitments = st.number_input("Monthly Commitments", min_value=0.0)
    dsr = st.slider("Debt Service Ratio (DSR)", 0.0, 1.5, 0.5)
    employment = st.selectbox("Employment Type", ["permanent", "contract", "self-employed"])
    high_networth = st.checkbox("High Net-Worth Customer")

    submitted = st.form_submit_button("Evaluate")

if submitted:
    case = LoanCase(
        case_id="CASE-001",
        monthly_income=income,
        monthly_commitments=commitments,
        dsr=dsr,
        employment_type=employment,
        is_high_networth=high_networth
    )

    result = evaluate(case)

    st.subheader("AI Recommendation")
    st.write(result.recommendation)

    st.subheader("Approve Flags")
    st.write(result.approve_flags)

    st.subheader("Reject Flags")
    st.write(result.reject_flags)

    if result.recommendation == "REVIEW":
        st.warning("Manual review required")
