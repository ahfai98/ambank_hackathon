import chromadb
from chromadb.utils import embedding_functions
import os

# Optional: force CPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Persistent Chroma client
client = chromadb.PersistentClient(path=".chromadb")

# Get collection
collection = client.get_collection("loan_policies")

# Create embedding function
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

def retrieve_policies(query, top_k=3):
    """
    Retrieve top_k most relevant policies for a given query
    """
    # NEW: use callable to get embedding
    query_embedding = embedding_function([query])[0]

    # Query Chroma
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    policies = []
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        policies.append({
            "text": doc,
            "source": meta.get("source", "unknown")
        })
    return policies
