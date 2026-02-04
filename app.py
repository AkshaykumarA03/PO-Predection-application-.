import streamlit as st
import json
import pandas as pd
from datetime import datetime
from classifier import classify_po
from taxonomy import TAXONOMY

st.set_page_config(page_title="PO Category Classifier", layout="wide")

# [cite_start]Styling remains consistent with your original design [cite: 1]
st.markdown(
    """
    <style>
      :root { --accent: #60a5fa; --bg: #0b1220; --border: #1e293b; --panel: #0f172a; --ink: #e2e8f0; }
      .block-container { padding-top: 1.2rem; }
      [data-testid="stAppViewContainer"] { background: var(--bg); }
      .hero-wrap {
        background: linear-gradient(135deg, #0f172a 0%, #0b1220 60%);
        border: 1px solid var(--border); padding: 20px; border-radius: 18px;
      }
      .muted { color: #94a3b8; font-size: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="hero-wrap"><h1>PO Category Classifier</h1><p>Classify single POs or batch upload files.</p></div>', unsafe_allow_html=True)

# Sidebar with Taxonomy Browser
with st.sidebar:
    st.subheader("Taxonomy Reference")
    with st.expander("View Available Categories"):
        st.text(TAXONOMY)
    st.markdown("---")
    
    # [cite_start]Examples logic [cite: 1]
    if st.button("Load Example"):
        st.session_state.po_description = "Purchase 10 cases of A4 printer paper"
        st.session_state.supplier = "Staples"

# Tabs for Single vs Batch
tab1, tab2 = st.tabs(["Single Classification", "Batch Processing"])

with tab1:
    left, right = st.columns([2, 1])
    with left:
        po_desc = st.text_area("PO Description", key="po_description", height=150)
        supp = st.text_input("Supplier (optional)", key="supplier")
    
    with right:
        if st.button("Classify Single", type="primary", use_container_width=True):
            if po_desc:
                with st.spinner("Analyzing..."):
                    result = classify_po(po_desc, supp)
                    try:
                        parsed = json.loads(result)
                        st.success("Classification Complete")
                        st.json(parsed)
                        # Confidence logic
                        conf = parsed.get("confidence", 0)
                        if isinstance(conf, float) and conf < 0.7:
                            st.warning(f"Low confidence score: {conf}")
                    except:
                        st.error("Invalid JSON returned from model.")

with tab2:
    st.subheader("Bulk Upload")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        st.write("Preview:", df.head(3))
        
        col_to_use = st.selectbox("Select Description Column", df.columns)
        
        if st.button("Run Batch Process"):
            results = []
            progress_bar = st.progress(0)
            for i, row in df.iterrows():
                raw_res = classify_po(str(row[col_to_use]))
                try:
                    results.append(json.loads(raw_res))
                except:
                    results.append({"L1": "Error", "L2": "Error", "L3": "Error", "confidence": 0})
                progress_bar.progress((i + 1) / len(df))
            
            res_df = pd.DataFrame(results)
            final_df = pd.concat([df, res_df], axis=1)
            st.dataframe(final_df)
            st.download_button("Download Results", final_df.to_csv(index=False), "classified_pos.csv")
