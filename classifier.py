import streamlit as st
from groq import Groq
import json
from prompts import SYSTEM_PROMPT, CHATBOT_PROMPT

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
MODEL_ID = "llama-3.1-8b-instant"

def classify_po(po_description: str, supplier: str = "Not provided"):
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            temperature=0.0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Description: {po_description}\nSupplier: {supplier}"}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"L1": "Error", "L2": "Error", "L3": "Error", "confidence": 0, "error": str(e)}

def get_chat_response(query: str, history: list):
    messages = [{"role": "system", "content": CHATBOT_PROMPT}]
    for msg in history[-5:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": query})
    
    try:
        response = client.chat.completions.create(model=MODEL_ID, temperature=0.5, messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        return f"I'm sorry, I encountered an error: {str(e)}"
