🌱 EcoPickup — AI Waste Pickup Booking Assistant

An end-to-end AI-powered application for waste pickup scheduling, PDF-based document question answering (RAG), voice-enabled chatbot, and a complete admin dashboard.
Built as part of the Neostats Round-2 AI Engineer assignment.

📌 Overview

EcoPickup is an AI-powered chatbot designed to make waste pickup services smart, fast, and automated.
Users can:

Book organic, plastic, paper, glass, e-waste, mixed waste, or microplastic sample pickups

Ask questions from uploaded PDFs using RAG

Receive voice-generated bot replies (TTS)

Receive detailed email confirmations

View and modify bookings using an admin portal

This project demonstrates strong knowledge in:

Conversational AI

Retrieval Augmented Generation (RAG)

Database design

Tool calling (DB, Email, RAG, Search)

Streamlit-based frontend engineering

Deployment on Streamlit Cloud

🔐 Admin Login Details

To access the Admin Dashboard:

Admin Password: admin123


(Admin credentials are safe because they DO NOT give access to any real system.)

🚀 Features
1️⃣ AI Chatbot (Groq LLaMA-3.1)

Detects booking intent

Collects user details conversationally

Uses short-term memory

Summarizes and confirms before saving

Prevents invalid inputs (email/date/time validation)

2️⃣ Booking Flow

The chatbot collects:

Name

Email

Phone

Pickup Type

Date

Time

Then:

✔ Shows summary
✔ Asks for confirmation
✔ Stores in database
✔ Sends email confirmation
✔ Plays voice output

3️⃣ RAG — PDF Q&A

Upload any number of PDFs

Extract text with pdfplumber

Chunk + embed using sentence-transformers

Store embeddings in FAISS

Answer user queries using LLaMA LLM with retrieved context

4️⃣ Admin Dashboard

View all bookings

Filter by name, date, email, type, status

Update booking status

Delete bookings

Export bookings to CSV

Pagination supported

5️⃣ Voice Output (Text-to-Speech)

Uses gTTS to generate bot voice

Every chatbot reply includes an audio player

6️⃣ Email Confirmation

Sent via SMTP after booking:

Includes:

Name

Booking ID

Type

Date & Time

Support info

EcoPickup website

7️⃣ Web Search Tool (Optional Tool)

DuckDuckGo instant search API:
Used when user explicitly asks for general info not found in RAG.

🛠️ Tech Stack
Component	Technology
Frontend	Streamlit
Backend	Python
LLM	Groq LLaMA-3.1 (via Groq API)
RAG	FAISS + Sentence Transformers
Email	SMTP
TTS	gTTS
PDF Parsing	pdfplumber
DB	SQLite (via SQLAlchemy)
📁 Project Structure
ecopickup/
│
├── app/
│   ├── main.py                  # Streamlit entry point
│   ├── chat_logic.py            # Intent detection + conversational logic
│   ├── booking_flow.py          # Slot filling + confirmation + validation
│   ├── rag_pipeline.py          # PDF ingestion + embeddings + FAISS
│   ├── tools.py                 # DB save, SMTP email, RAG tool, TTS, web search
│   ├── admin_dashboard.py       # Complete admin panel
│
├── db/
│   ├── database.py              # SQLite setup
│   └── models.py                # SQLAlchemy ORM models
│
├── docs/                        # Sample PDFs + diagrams
│
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml (NOT IN REPO — only in deployment)

🔧 Installation Instructions
1. Clone the repository
git clone https://github.com/nandana1318biju/EcoPickup-AI-Booking-Assistant.git
cd EcoPickup-AI-Booking-Assistant

2. Install dependencies
pip install -r requirements.txt

3. Add Streamlit Secrets

Create:
.streamlit/secrets.toml

[groq]
api_key = "YOUR_GROQ_API_KEY"

[smtp]
host = "smtp.gmail.com"
port = 587
user = "your@gmail.com"
pass = "your_gmail_app_password"

4. Run the app
streamlit run app/main.py

🌐 Live Demo (Streamlit Cloud)

🔗 Live App URL:
👉 Add your Streamlit Cloud link here after deployment

📸 Screenshots (Add after deployment)

Chatbot Interface

PDF Upload

Booking Confirmation

Admin Dashboard

Status Update

CSV Export

Voice Output Button

(You can add these after deploying.)

🧠 How It Works — Architecture
User → Streamlit Chat UI
       → Intent Detection (RAG / Booking / General / Search)
          → Booking Flow → SQLite DB + Email + TTS
          → RAG Pipeline → FAISS → LLaMA Model → Answer
          → Web Search Tool → DuckDuckGo

🎯 Use Case Explanation & Project Purpose

EcoPickup solves a real problem:

People often struggle with proper waste management, scheduling pickups, or understanding recycling rules.

This system:

✔ Automates the entire pickup process

No forms. No apps. Pure conversation.

✔ Provides instant answers

Users can upload government guidelines or waste policy PDFs and ask questions.

✔ Supports microplastic research workflows

A special “microplastic sample pickup” type is included to align with your background.

✔ Gives organizations an admin dashboard

Admins can update or delete bookings, filter by date, export reports, and more.

✔ Adds accessibility via voice output

Visually impaired users benefit from TTS playback.

🏁 Future Improvements

Add STT (voice input)

Multi-location support

Live vehicle tracking

Notifications via WhatsApp

Multi-admin roles

Supabase cloud database

❤️ Built By

Nandana Biju
MSc AI & ML
Christ University
