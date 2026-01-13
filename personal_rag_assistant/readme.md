### Personal RAG Assistant

Building a local RAG (Retrieval-Augmented Generation) system using Ollama, LangChain, and Streamlit while leveraging powerful LLMs.

```bash
personal_rag_assistant/
├── personal_rag_assistant.py  # Streamlit UI and session management
├── rag_system.py       # Core RAG logic (Embeddings, Vector Store, LLM)
├── config.py           # Configuration and constants
├── requirements.txt    # Python dependencies
└── data/               # (Auto-created) Local ChromaDB storage
```

### Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Ollama Installation and Model Downloads

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull nomic-embed-text
ollama pull gemma3
```

### Run Streamlite
streamlit run personal_rag_assistant.py