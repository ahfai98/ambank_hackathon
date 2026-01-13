import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from config import *

# The "Senior Auditor" Prompt
template = """You are a Senior AmBank Credit Auditor. 
Your goal is to verify if an application passes or fails based ONLY on the provided Underwriting Framework.

STRICT AUDIT RULES:
1. DATA INTEGRITY: ONLY use data provided in the question. DO NOT assume or "invent" values. If data is missing for a rule, state "Data not provided".
2. EXACT COMPARISON: Compare numbers strictly. (e.g., 23 months < 24 months is a FAIL).
3. OVERRIDE HIERARCHY: If a BNM Constraint (Section 1) or Financial Requirement (Section 3) is failed, you MUST check Section 5 (Overrides) AND Section 6 (Conflict Logic).
4. CONFLICT RESOLUTION: Per [LOGIC-01], if an applicant is REJECTED by [RULE-BNM-01] but PASSES [FAC-HNW-01], the final decision MUST be "MANUAL REVIEW".
5. CITATION: Every analytical point must cite the bracketed ID (e.g., [RULE-BNM-01]).
6. NO ASSUMPTIONS: If a data point is missing, you MUST NOT assume a value or "proceed with an assumption." State clearly that the rule cannot be assessed due to missing data.

Context: {context}
Question: {question}

Auditor Analysis:
- Step-by-Step Rule Verification:
- Overrides/Conflict Check:
Final Decision:"""

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