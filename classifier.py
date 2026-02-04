import streamlit as st
from groq import Groq
from prompts import SYSTEM_PROMPT

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def classify_po(po_description: str, supplier: str = "Not provided"):
    user_prompt = f"PO Description: {po_description}\nSupplier: {supplier}"
    
    # Use Llama-3.1-8b as specified in your requirements
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.0,
        # Force JSON output mode
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content
