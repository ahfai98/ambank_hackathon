import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from config import *

# The "Senior Auditor" Prompt
template = """You are a Deterministic Credit Logic Engine. Your goal is to populate a scorecard and determine the final verdict using the following logic gates:

### 1. SELECTION OPTIONS:
- **YES**: Data meets or exceeds the policy requirement.
- **NO**: Data fails the requirement (standard).
- **HARD REJECT**: Data fails a strict regulatory or demographic mandate.
- **OVERRIDE**: Data triggers a specific policy allowance (e.g., Section 5) that can mitigate a NO or HARD REJECT.
- **DATA NOT AVAILABLE**: Information was not provided in the applicant's profile.

### 2. VERDICT HIERARCHY:
- **Rule A (The Override Rule)**: If any box is [OVERRIDE] AND any other box is [NO] or [HARD REJECT] -> **VERDICT: MANUAL REVIEW**.
- **Rule B (The Hard Stop)**: If there is at least one [HARD REJECT] AND zero [OVERRIDE] boxes -> **VERDICT: HARD NO**.
- **Rule C (The Majority Rule)**: If no [HARD REJECT] or [OVERRIDE] exists:
    - Majority [YES] -> **VERDICT: CLEAR YES**
    - Majority [NO] -> **VERDICT: HARD NO**

### SCORECARD TABLE:
[Policy ID] | [Requirement] | [Applicant Data] | [Math/Logic Check] | [Selection] | [Source Trace]
--- | --- | --- | --- | --- | ---

### DATA TO ANALYZE:
Context: {context}
Question: {question}

### AUDIT SCORECARD:"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

class RAGEngine:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        self.llm = OllamaLLM(model=LLM_MODEL)
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)

    def process_pdf(self, file_path):
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\nSECTION", "\n- [", "\n\n", "\n", " "]
        )
        chunks = splitter.split_documents(docs)
        
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            client=self.client,
            collection_name=COLLECTION_NAME
        )
        return vectorstore

    def get_qa_chain(self):
        try:
            collection = self.client.get_collection(COLLECTION_NAME)
            if collection.count() == 0:
                return None
        except Exception:
            return None

        vectorstore = Chroma(
            client=self.client,
            collection_name=COLLECTION_NAME,
            embedding_function=self.embeddings
        )
        
        # return_source_documents=True is vital for the UI expander
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 7}),
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
            return_source_documents=True 
        )

    def clear_all_data(self):
        try:
            self.client.delete_collection(COLLECTION_NAME)
            self.client.create_collection(COLLECTION_NAME)
            return True
        except Exception as e:
            print(f"Error clearing collection: {e}")
            return False