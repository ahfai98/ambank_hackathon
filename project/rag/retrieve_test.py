from rag.retrieve import retrieve_policies

query = """
Monthly Income: 5000
Monthly Commitments: 4500
DSR: 0.9
Employment Type: permanent
High Net-Worth: True
"""

policies = retrieve_policies(query, top_k=3)

for i, p in enumerate(policies, start=1):
    print(f"Policy {i} ({p['source']}):\n{p['text']}\n{'-'*50}")
