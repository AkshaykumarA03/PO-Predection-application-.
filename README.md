PO L1–L2–L3 Category Classifier

This project is a Streamlit-based AI application that classifies Purchase Order (PO) descriptions into L1, L2, and L3 categories using a fixed enterprise taxonomy and a Groq-hosted LLM.

Overview

The application takes a PO description (and optional supplier name) and returns a strict JSON response containing the most appropriate L1, L2, and L3 categories.
The model is constrained to use only the provided taxonomy and returns "Not sure" when classification is unclear.

How the System Works

app.py provides the Streamlit user interface

User input is sent to the classifier

classifier.py calls the Groq LLM (llama-3.1-8b-instant)

prompts.py enforces strict classification rules and JSON output

taxonomy.py defines the allowed L1–L2–L3 categories

The result is displayed as structured JSON in the UI

Project Structure
app.py          # Streamlit UI
classifier.py   # LLM classification logic
prompts.py      # System prompt and examples
taxonomy.py     # Enterprise taxonomy

Features

L1, L2, L3 PO classification

Fixed enterprise taxonomy enforcement

JSON-only output (no explanations)

Optional supplier input

Deterministic results (temperature = 0.0)

Tech Stack

Python

Streamlit

Groq API

LLaMA 3.1 (8B Instant)

JSON-based structured responses

Setup & Run

Install dependencies:

pip install streamlit groq


Configure Groq API key in .streamlit/secrets.toml:

GROQ_API_KEY = "your_api_key_here"


Run the app:

streamlit run app.py

Example Output
{
  "po_description": "DocuSign Inc - eSignature Enterprise Pro Subscription",
  "L1": "IT",
  "L2": "Software",
  "L3": "Subscription"
}

Classification Rules

Uses only predefined taxonomy

Does not invent categories

Does not mix categories across rows

Returns "Not sure" if unclear

Always outputs valid JSON
