import streamlit as st
from rag.retrieve import retrieve_policies

st.set_page_config(page_title="Loan Policy Explainer Phase 2", layout="centered")
st.title("Ambank Explainable AI - Phase 2 Demo")
st.write(
    "Enter a loan application scenario below to see which bank policies are relevant."
)

# Input text area for loan case
query = st.text_area(
    "Loan Case Input",
    value="""Monthly Income: 5000
Monthly Commitments: 4500
DSR: 0.9
Employment Type: permanent
High Net-Worth: True""",
    height=200,
)

top_k = st.slider("Number of policies to retrieve:", 1, 10, 3)

if st.button("Retrieve Relevant Policies"):
    if query.strip() == "":
        st.warning("Please enter a loan case scenario.")
    else:
        with st.spinner("Retrieving policies..."):
            policies = retrieve_policies(query, top_k=top_k)

        if not policies:
            st.info("No policies found for this query.")
        else:
            st.success(f"Found {len(policies)} relevant policies:")
            for i, p in enumerate(policies, start=1):
                st.markdown(f"**Policy {i} ({p['source']})**")
                st.markdown(f"> {p['text']}")
                st.markdown("---")
