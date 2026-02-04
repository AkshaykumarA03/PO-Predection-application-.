import streamlit as st
from groq import Groq
from prompts import SYSTEM_PROMPT, CHATBOT_PROMPT
import json

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def classify_po(po_description: str, supplier: str = "Not provided"):
    user_prompt = f"PO Description: {po_description}\nSupplier: {supplier}"
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.0, # Deterministic for classification
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )
    return json.loads(response.choices[0].message.content)

def get_chat_response(query, history):
    # Context-aware chatbot
    context = f"Current classification history: {json.dumps(history[:3])}"
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": CHATBOT_PROMPT},
            {"role": "user", "content": f"Context: {context}\nUser Query: {query}"}
        ]
    )
    return response.choices[0].message.content
