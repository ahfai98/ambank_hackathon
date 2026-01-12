from rag.retrieve import retrieve_policies
from utils.llm import explain
from models.decision_result import DecisionResult

def generate_explanation(case_dict: dict, result: DecisionResult) -> str:
    """
    Generates a human-readable explanation citing policies
    """
    # Convert LoanCase to simple query string
    query = f"""
    Monthly Income: {case_dict['monthly_income']}
    Monthly Commitments: {case_dict['monthly_commitments']}
    DSR: {case_dict['dsr']}
    Employment Type: {case_dict['employment_type']}
    High Net-Worth: {case_dict['is_high_networth']}
    """
    # Retrieve relevant policies
    policies = retrieve_policies(query)

    # Build prompt for LLM
    policy_text = "\n".join([f"{p['source']}: {p['text']}" for p in policies])
    prompt = f"""
    Given the loan case:
    {query}

    And the following policies:
    {policy_text}

    Explain why each approve/reject flag was triggered.
    Output concise, plain language explanation.
    """
    explanation = explain(prompt)
    return explanation
