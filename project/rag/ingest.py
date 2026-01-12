import os
import chromadb
from chromadb.utils import embedding_functions

# Optionally force CPU (suppress GPU warning)
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Policy folders
BASE_POLICY_PATH = "data/policies/base/"
SUGGESTED_POLICY_PATH = "data/policies/suggested/"

# Create a persistent ChromaDB client
client = chromadb.PersistentClient(path=".chromadb")  # <–– correct

# Safely delete old collection if exists
try:
    client.delete_collection("loan_policies")
    print("Old collection deleted.")
except chromadb.errors.NotFoundError:
    print("Collection 'loan_policies' does not exist yet, creating a new one...")

collection = client.get_or_create_collection("loan_policies")

# Embedding function  
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def embed_policy_folder(folder_path, label_prefix):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r") as f:
                text = f.read()
                collection.add(
                    documents=[text],
                    metadatas=[{"source": f"{label_prefix}/{filename}"}],
                    ids=[f"{label_prefix}_{filename}"]
                )
    print(f"Embedded policies from", folder_path)

# Run ingestion
embed_policy_folder(BASE_POLICY_PATH, "base")
embed_policy_folder(SUGGESTED_POLICY_PATH, "suggested")
print("Policy embeddings ingested successfully.")
