import streamlit as st
import pandas as pd
import json
from datetime import datetime
from classifier import classify_po, get_chat_response

st.set_page_config(page_title="PO Intelligence", layout="wide")

# Premium Dark Theme CSS
st.markdown("""
    <style>
    .stApp { background-color: #0b1220; color: white; }
    [data-testid="stSidebar"] { background-color: #0f172a; }
    .stMetric { background: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    </style>
""", unsafe_allow_html=True)

if "history" not in st.session_state: st.session_state.history = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "I'm your PO Sidekick. How can I help?"}]

# --- SIDEBAR CHAT ---
with st.sidebar:
    st.title("🤖 PO Sidekick")
    chat_container = st.container(height=400)
    for msg in st.session_state.chat_history:
        chat_container.chat_message(msg["role"]).write(msg["content"])
    
    if prompt := st.chat_input("Ask about taxonomy..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        chat_container.chat_message("user").write(prompt)
        answer = get_chat_response(prompt, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        chat_container.chat_message("assistant").write(answer)

# --- MAIN DASHBOARD ---
st.title("🏢 PO Intelligence & Classification")
t1, t2 = st.tabs(["🚀 Individual / Bulk", "📜 History & Export"])

with t1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Manual Entry")
        desc = st.text_area("PO Description")
        supp = st.text_input("Supplier")
        if st.button("Classify PO"):
            result = classify_po(desc, supp)
            st.session_state.history.insert(0, result)
            st.json(result)
            
    with col2:
        st.subheader("Bulk Upload")
        file = st.file_uploader("Upload CSV/Excel", type=['csv', 'xlsx'])
        if file and st.button("Run Batch Process"):
            st.warning("Processing large batches may take a moment...")
            # Logic for looping through rows would go here

with t2:
    if st.session_state.history:
        st.dataframe(pd.DataFrame(st.session_state.history))
        st.download_button("Export JSON", json.dumps(st.session_state.history), "po_export.json")
