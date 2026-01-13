import streamlit as st
import os
from rag_system import RAGEngine

st.set_page_config(page_title="AmBank Auditor Assistant", layout="wide")
st.title("🛡️ AmBank Underwriting Assistant")

if "engine" not in st.session_state:
    st.session_state.engine = RAGEngine()

engine = st.session_state.engine

# --- Sidebar ---
with st.sidebar:
    st.header("Document Management")
    uploaded_file = st.file_uploader("Upload Policy PDF", type="pdf")
    
    if st.button("Index Document") and uploaded_file:
        with st.spinner("Analyzing and Chunking..."):
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            engine.process_pdf(temp_path)
            os.remove(temp_path)
            st.success("Policy Loaded into Vector DB!")

    st.divider()
    if st.button("Clear Audit History", type="primary"):
        if engine.clear_all_data():
            st.session_state.messages = []
            st.success("Database Purged!")
            st.rerun()

# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history with saved evidence
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "evidence" in message:
            with st.expander("📂 View Cited Context"):
                st.info(message["evidence"])

# Input Logic
if prompt := st.chat_input("Enter application scenario..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chain = engine.get_qa_chain()
        if chain:
            with st.spinner("Consulting Framework..."):
                # chain returns a dict because of return_source_documents=True
                response = chain.invoke(prompt)
                answer = response["result"]
                sources = response["source_documents"]

                st.markdown(answer)

                # Generate the Evidence Text for the Expander
                evidence_text = ""
                for i, doc in enumerate(sources):
                    page_num = doc.metadata.get('page', 'Unknown')
                    evidence_text += f"**Source Chunk {i+1} (Page {page_num}):**\n{doc.page_content}\n\n---\n"
                
                with st.expander("📂 View Policy Evidence"):
                    st.info("The Auditor analyzed these sections to reach the decision:")
                    st.markdown(evidence_text)

                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "evidence": evidence_text
                })
        else:
            st.warning("Please upload a policy document to begin the audit.")