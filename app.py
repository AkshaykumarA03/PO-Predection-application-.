import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import datetime
from io import BytesIO
from classifier import classify_po, get_chat_response
from taxonomy import TAXONOMY

# 1. Page Configuration & Premium Theme
st.set_page_config(
    page_title="PO Intel | Enterprise Classifier",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern SaaS Look
st.markdown("""
    <style>
    .main { background: #0b1220; }
    .stMetric { background: #1e293b; padding: 15px; border-radius: 12px; border: 1px solid #334155; }
    div[data-testid="stSidebar"] { background-color: #0f172a; border-right: 1px solid #1e293b; }
    .stButton>button { width: 100%; border-radius: 8px; background: linear-gradient(90deg, #3b82f6, #2563eb); color: white; border: none; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #1e293b; border-radius: 8px 8px 0 0; padding: 10px 20px; }
    </style>
""", unsafe_allow_html=True)

# 2. Session State Initialization
if "history" not in st.session_state: st.session_state.history = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [{"role": "assistant", "content": "Hello! I'm your PO Intelligence assistant. How can I help you with procurement or classification today?"}]

# 3. Sidebar: Persistent AI Chatbot
with st.sidebar:
    st.title("🤖 PO Sidekick")
    st.caption("AI Assistant for Procurement Workflows")
    
    chat_container = st.container(height=400)
    for msg in st.session_state.chat_messages:
        chat_container.chat_message(msg["role"]).write(msg["content"])
    
    if chat_input := st.chat_input("Ask about taxonomy or results..."):
        st.session_state.chat_messages.append({"role": "user", "content": chat_input})
        chat_container.chat_message("user").write(chat_input)
        
        with chat_container.chat_message("assistant"):
            response = get_chat_response(chat_input, st.session_state.history)
            st.write(response)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})

    st.divider()
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()

# 4. Main Dashboard Layout
st.title("🏢 PO Intelligence Dashboard")
st.markdown("### Production-Grade Enterprise Classification")

tab1, tab2, tab3 = st.tabs(["🚀 Classification", "📊 Analytics", "📜 History"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Single Classification")
        po_desc = st.text_area("PO Description", placeholder="e.g., Annual subscription for Salesforce CRM licenses")
        supplier = st.text_input("Supplier (Optional)", placeholder="e.g., Salesforce.com Inc.")
        
        if st.button("Analyze PO"):
            if po_desc:
                with st.spinner("Classifying..."):
                    result = classify_po(po_desc, supplier)
                    st.session_state.history.insert(0, {**result, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%S")})
                    st.success("Classification Complete!")
                    st.json(result)
            else:
                st.error("Please enter a description.")

    with col2:
        st.subheader("Bulk Processing")
        uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('csv') else pd.read_excel(uploaded_file)
            st.dataframe(df.head())
            if st.button("Process Batch"):
                # Implementation for batch LLM calls would go here
                st.info("Batch processing initiated. Results will appear in history.")

with tab2:
    if st.session_state.history:
        h_df = pd.DataFrame(st.session_state.history)
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Analyzed", len(h_df))
        c2.metric("Avg Confidence", f"{h_df['confidence'].mean():.2%}")
        c3.metric("Top L1", h_df['L1'].mode()[0])
        
        fig = px.pie(h_df, names='L1', title='Category Distribution (L1)', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for analytics. Run a classification first.")

with tab3:
    if st.session_state.history:
        st.dataframe(st.session_state.history, use_container_width=True)
        # Download Button
        json_data = json.dumps(st.session_state.history, indent=2)
        st.download_button("Download Full History (JSON)", data=json_data, file_name="po_history.json", mime="application/json")
    else:
        st.write("No history records found.")
