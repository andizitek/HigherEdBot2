import streamlit as st
import os
import openai
from dotenv import load_dotenv
import PyPDF2

# Lade Umgebungsvariablen
load_dotenv()
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = os.getenv("AZURE_API_KEY")
openai.api_version = "2024-02-15-preview"
deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")

# Streamlit App
st.set_page_config(page_title="PDF-Chat mit GPT-4o", layout="wide")
st.title("📄 Chat mit deiner PDF")

# PDF hochladen
uploaded_file = st.file_uploader("Lade eine PDF hoch", type="pdf")

if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    st.success("PDF wurde erfolgreich gelesen.")

    # Eingabe für Frage
    question = st.text_input("Stelle eine Frage zum PDF-Inhalt:")

    if question:
        with st.spinner("GPT-4o denkt nach..."):
            messages = [
                {
                    "role": "system",
                    "content": f"""Du bist ein hilfreicher Assistent. Beantworte die Frage ausschließlich auf Basis des folgenden Textes:
                    
                    TEXT:
                    {text}
                    
                    Wenn du keine Antwort im Text findest, gib das bitte ehrlich an."""
                },
                {"role": "user", "content": question}
            ]

            response = openai.ChatCompletion.create(
                engine=deployment_name,
                messages=messages,
                temperature=0.2
            )

            st.subheader("💬 Antwort:")
            st.write(response["choices"][0]["message"]["content"])
