import streamlit as st
from rag.retrieve import retrieve_policies
import sqlite3
import datetime
import os

st.set_page_config(page_title="Loan Policy Explainer Phase 3", layout="centered")
st.title("Ambank Explainable AI - Phase 3 Demo")
st.write(
    "Enter a loan case scenario to retrieve relevant policies. "
    "If conflicting flags are detected, an officer review is required."
)

# ---------- DATABASE FUNCTIONS ----------

DB_PATH = "officer_reviews.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            case_id TEXT PRIMARY KEY,
            query_text TEXT,
            retrieved_policies TEXT,
            decision TEXT,
            notes TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_officer_review(case_id, query_text, retrieved_policies, decision, notes):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO reviews (case_id, query_text, retrieved_policies, decision, notes, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (case_id, query_text, ",".join(retrieved_polic_
