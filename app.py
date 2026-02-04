import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import datetime
from classifier import classify_po, get_chat_response

# 1. Page Config
st.set_page_config(page_title="PO Intelligence Pro", page_icon="💎", layout="wide")

# 2. Advanced Custom CSS (Colorful & Modern)
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Gradient Header Card */
    .header-card {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(10px);
        border-right: 1px solid #334155;
    }

    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid #475569;
        padding: 20px;
        border-radius: 12px;
        transition: transform 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #60a5fa;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #1e293b;
        border-radius: 8px 8px 0px 0px;
        color: white;
        padding: 0 20px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(0deg, #3b82f6, #2563eb) !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        border: none;
        color: white;
        font-weight: 600;
        padding: 0.6rem 2rem;
        border-radius: 8px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        opacity: 0.9;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Session State
if "history" not in st.session_state: st.session_state.history = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "Welcome! I'm your PO Sidekick. How can I help you classify today?"}]

# 4. Sidebar: AI Chatbot (Glassmorphic)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("PO Sidekick")
    st.markdown("---")
    
    chat_container = st.container(height=450)
    for msg in st.session_state.chat_history:
        chat_container.chat_message(msg["role"]).write(msg["content"])
    
    if prompt := st.chat_input("Ask about taxonomy..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        chat_container.chat_message("user").write(prompt)
        
        with st.spinner("Thinking..."):
            answer = get_chat_response(prompt, st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            chat_container.chat_message("assistant").write(answer)

# 5. Main Dashboard Body
st.markdown('<div class="header-card"><h1>💎 PO Intelligence & Classification</h1><p>Enterprise AI-powered spend categorization</p></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🚀 Classification Engine", "📊 Visual Analytics", "📜 Audit History"])

with tab1:
    c1, c2 = st.columns([1, 1.2], gap="large")
    
    with c1:
        st.subheader("📝 New Analysis")
        with st.form("input_form"):
            po_desc = st.text_area("PO Description", height=150, placeholder="e.g., Annual subscription for 500 Zoom Enterprise licenses...")
            supplier = st.text_input("Supplier Name", placeholder="e.g., Zoom Video Communications")
            submitted = st.form_submit_button("Analyze Line Item")
            
            if submitted and po_desc:
                with st.spinner("🤖 LLM Engine Processing..."):
                    result = classify_po(po_desc, supplier)
                    result['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    st.session_state.history.insert(0, result)
                    st.toast("Classification Successful!", icon="✅")

    with c2:
        if st.session_state.history:
            latest = st.session_state.history[0]
            st.subheader("🎯 Latest Result")
            
            res_col1, res_col2 = st.columns(2)
            res_col1.metric("L1 Category", latest.get('L1', 'N/A'))
            res_col2.metric("Confidence", f"{int(float(latest.get('confidence', 0))*100)}%")
            
            st.markdown(f"**L2:** `{latest.get('L2')}` | **L3:** `{latest.get('L3')}`")
            st.json(latest)
        else:
            st.info("👈 Enter PO details to begin classification.")

with tab2:
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.subheader("📈 Classification Insights")
        
        col_a, col_b = st.columns(2)
        with col_a:
            fig1 = px.pie(df, names='L1', hole=0.5, title="Spend by L1 Sector", color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig1, use_container_width=True)
        with col_b:
            fig2 = px.histogram(df, x='confidence', title="Confidence Score Distribution", color_discrete_sequence=['#8b5cf6'])
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No data available. Run some classifications first.")

with tab3:
    if st.session_state.history:
        st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
        csv = pd.DataFrame(st.session_state.history).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export to CSV", data=csv, file_name="po_history.csv", mime="text/csv")
    else:
        st.write("History is currently empty.")
