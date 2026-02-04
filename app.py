import streamlit as st
import json
from classifier import classify_po

# Setup
st.set_page_config(page_title="PO Classifier", layout="wide", page_icon="🏷️")

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_p=True)

st.title("🏷️ Smart PO Categorizer")
st.caption("AI-powered Level 1, 2, and 3 taxonomy classification")

# Sidebar for metadata/settings
with st.sidebar:
    st.header("Settings")
    st.info("This tool uses the L1-L2-L3 framework to organize procurement spend.")
    if st.button("Clear History"):
        st.rerun()

# Layout: 2 Columns for Input/Output
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Input Details")
    with st.container(border=True):
        po_description = st.text_area("PO Description", height=150, placeholder="Describe the items or services...")
        supplier = st.text_input("Supplier Name (Optional)")
        classify_btn = st.button("Run Classification", type="primary", use_container_width=True)

with col2:
    st.subheader("Classification Results")
    if classify_btn:
        if not po_description.strip():
            st.warning("Please enter a description.")
        else:
            with st.spinner("Analyzing taxonomy..."):
                # Mocking the result structure for the UI demo
                # result = classify_po(po_description, supplier)
                try:
                    # Logic assumes result is a dict or JSON string with L1, L2, L3 keys
                    data = json.loads(classify_po(po_description, supplier))
                    
                    # Displaying L1, L2, L3 as clean metrics
                    m_col1, m_col2, m_col3 = st.columns(3)
                    m_col1.metric("Level 1", data.get("L1", "N/A"))
                    m_col2.metric("Level 2", data.get("L2", "N/A"))
                    m_col3.metric("Level 3", data.get("L3", "N/A"))
                    
                    with st.expander("View Raw JSON Response"):
                        st.json(data)
                        
                except Exception as e:
                    st.error("Could not parse classification.")
                    st.info(f"Raw Output: {classify_po(po_description, supplier)}")
    else:
        st.info("Waiting for input... Fill out the form on the left to see results.")
