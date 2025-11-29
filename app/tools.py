# app/tools.py

import streamlit as st
from groq import Groq
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from db.database import SessionLocal
from db.models import Customer, Booking
from sqlalchemy.exc import SQLAlchemyError
import datetime
import requests

from app.rag_pipeline import add_documents_from_uploaded_files, rag_answer
from gtts import gTTS
import base64

# ------------------------------
# Save booking to DB
# ------------------------------
def save_booking_to_db(data):
    db = SessionLocal()
    try:
        customer = (
            db.query(Customer)
            .filter(Customer.email == data["email"])
            .first()
        )

        if not customer:
            customer = Customer(
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)

        booking = Booking(
            customer_id=customer.customer_id,
            booking_type=data["pickup_type"],
            date=data["date"],
            time=data["time"],
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


# ------------------------------
# Email sending (SMTP)
# ------------------------------
def send_confirmation_email(to_email, subject, body):
    try:
        smtp_host = st.secrets["smtp"]["host"]
        smtp_port = st.secrets["smtp"]["port"]
        smtp_user = st.secrets["smtp"]["user"]
        smtp_pass = st.secrets["smtp"]["pass"]

        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()

        return {"success": True}

    except Exception as e:
        return {"success": False, "error": str(e)}


# ------------------------------
# LLM Completion (Groq)
# ------------------------------
def llm_complete(prompt, max_tokens=256, temperature=0.2):
    try:
        api_key = st.secrets["groq"]["api_key"]
    except:
        return "⚠ No Groq API key in secrets."

    client = Groq(api_key=api_key)

    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return res.choices[0].message["content"]

    except Exception as e:
        return f"LLM Error: {e}"


# ------------------------------
# RAG Tools
# ------------------------------
def rag_ingest_files(files):
    return add_documents_from_uploaded_files(files)

def rag_tool(query):
    rag_res = rag_answer(query)
    if not rag_res["success"]:
        return {"success": False, "answer": rag_res["answer"]}

    answer = llm_complete(rag_res["prompt"])
    return {"success": True, "answer": answer, "sources": rag_res["sources"]}


# ------------------------------
# Web Search Tool (DuckDuckGo)
# ------------------------------
def web_search_tool_duckduckgo(query, max_results=5):
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
        return {"success": False, "error": str(e)}

    answer = data.get("AbstractText")
    if answer:
        return {
            "success": True,
            "answer": answer,
            "sources": [{"source": data.get("AbstractURL", ""), "text": answer}],
        }

    return {"success": False, "error": "No useful results found."}


# ------------------------------
# TTS (gTTS)
# ------------------------------
def text_to_speech(text):
    tts = gTTS(text)
    tts.save("audio.mp3")

    audio_bytes = open("audio.mp3", "rb").read()
    b64 = base64.b64encode(audio_bytes).decode()
    return f"""
        <audio controls>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """


