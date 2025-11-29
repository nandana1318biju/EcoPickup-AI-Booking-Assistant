# app/tools.py

from db.database import SessionLocal
from db.models import Customer, Booking
from sqlalchemy.exc import SQLAlchemyError
import datetime
import streamlit as st
from groq import Groq
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests


# ------------------------------------------------------------
# SAVE BOOKING TO DATABASE
# ------------------------------------------------------------
def save_booking_to_db(booking_data):
    db = SessionLocal()

    try:
        # Check if customer exists
        existing_customer = (
            db.query(Customer).filter(Customer.email == booking_data["email"]).first()
        )

        if existing_customer:
            customer = existing_customer
        else:
            customer = Customer(
                name=booking_data["name"],
                email=booking_data["email"],
                phone=booking_data["phone"],
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)

        # New booking entry
        booking = Booking(
            customer_id=customer.customer_id,
            booking_type=booking_data["pickup_type"],
            date=booking_data["date"],
            time=booking_data["time"],
            status="confirmed",
            created_at=datetime.datetime.utcnow(),
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return {"success": True, "booking_id": booking.id}

    except SQLAlchemyError as e:
        db.rollback()
        return {"success": False, "error": str(e)}

    finally:
        db.close()


# ------------------------------------------------------------
# SEND EMAIL CONFIRMATION (SMTP)
# ------------------------------------------------------------
def send_confirmation_email(to_email, subject, body):
    try:
        smtp_host = st.secrets["smtp"]["host"]
        smtp_port = st.secrets["smtp"]["port"]
        smtp_user = st.secrets["smtp"]["user"]
        smtp_pass = st.secrets["smtp"]["pass"]

        message = MIMEMultipart()
        message["From"] = smtp_user
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to_email, message.as_string())
        server.quit()

        return {"success": True}

    except Exception as e:
        return {"success": False, "error": str(e)}


# ------------------------------------------------------------
# LLM COMPLETION USING GROQ (Corrected)
# ------------------------------------------------------------
def llm_complete(prompt: str, max_tokens: int = 256, temperature: float = 0.1):
    """
    Calls Groq LLaMA 3.3 70B model to generate RAG answers.
    """

    # Get GROQ API key
    try:
        api_key = st.secrets["groq"]["api_key"]
    except Exception:
        return "⚠ No GROQ API key found. Add it in .streamlit/secrets.toml."

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        # CORRECT extraction for Groq SDK
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ LLM Error: {e}"


# ------------------------------------------------------------
# RAG FILE INGEST + TOOL WRAPPER
# ------------------------------------------------------------
from app.rag_pipeline import add_documents_from_uploaded_files, rag_answer

def rag_ingest_files(uploaded_files):
    return add_documents_from_uploaded_files(uploaded_files)


def rag_tool(query: str, top_k: int = 4):
    """
    High-level RAG tool that merges vector retrieval + LLM generation.
    """
    rag_res = rag_answer(query, top_k=top_k)

    if not rag_res.get("success"):
        return {"success": False, "answer": "No documents indexed."}

    prompt = rag_res["prompt"]
    sources = rag_res.get("sources", [])

    answer = llm_complete(prompt)

    return {"success": True, "answer": answer, "sources": sources}

def web_search_tool_duckduckgo(query: str, max_results: int = 5):
    """
    Lightweight web search using DuckDuckGo Instant Answer API.
    Returns a dict: {success, answer (string), sources (list of dicts)}
    """
    try:
        params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "no_redirect": 1,
        }
        resp = requests.get("https://api.duckduckgo.com/", params=params, timeout=8)
        data = resp.json()
    except Exception as e:
        return {"success": False, "error": f"Search failed: {e}"}

    # Prefer AbstractText if present
    answer_parts = []
    sources = []

    abstract = data.get("AbstractText") or ""
    abstract_url = data.get("AbstractURL")
    if abstract:
        answer_parts.append(abstract)
        if abstract_url:
            sources.append({"source": abstract_url, "text": abstract})

    # RelatedTopics is often a list of topics with Text/FirstURL
    related = data.get("RelatedTopics", []) or []
    count = 0
    for item in related:
        if count >= max_results:
            break
        # items can be nested
        text = item.get("Text") or item.get("Name")
        url = item.get("FirstURL") or item.get("Result")
        if text:
            answer_parts.append(text)
            if url:
                sources.append({"source": url, "text": text})
                count += 1

    # If nothing useful, fallback to AbstractURL or just say no results
    if not answer_parts:
        return {"success": False, "error": "No concise results found."}

    # Combine into short answer
    answer = "\n\n".join(answer_parts[:6])
    return {"success": True, "answer": answer, "sources": sources[:max_results]}

# ------------------------------------------------------------
# TEXT-TO-SPEECH (TTS) USING gTTS
# ------------------------------------------------------------
from gtts import gTTS
import base64

def text_to_speech(text: str):
    """
    Converts text to speech and returns HTML audio player.
    Works on Streamlit Cloud.
    """
    try:
        tts = gTTS(text)
        tts.save("response_audio.mp3")

        audio_file = open("response_audio.mp3", "rb").read()
        b64 = base64.b64encode(audio_file).decode()

        audio_html = f"""
            <audio controls autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """
        return audio_html

    except Exception as e:
        return f"Audio generation failed: {e}"

