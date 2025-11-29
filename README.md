🌱EcoPickup — AI Waste Pickup Booking Assistant

An end-to-end AI-powered application for:

Waste pickup scheduling

Document-based Q&A using RAG

Voice-enabled chatbot (TTS)

Email confirmations

Complete Admin Dashboard

Deployment-ready Streamlit Cloud app

⭐ Overview

EcoPickup is an AI chatbot designed to make waste pickup services smart, fast, and automated.

Users can:

Book organic, plastic, paper, glass, e-waste, mixed waste, or microplastic sample pickups

Ask questions from uploaded PDFs using RAG

Receive voice-generated AI replies (TTS)

Receive email confirmations

View & modify bookings in an Admin Portal

This project demonstrates strong skills in:

Conversational AI

Retrieval Augmented Generation (RAG)

Database design (SQLite + SQLAlchemy)

Tool calling (DB, Email, RAG, Web Search)

Streamlit front-end engineering

Deployment on Streamlit Cloud

🔐 Admin Login Details

To access the Admin Dashboard:

**Admin Password: admin123**

These credentials are safe — admin panel is isolated and does not access any sensitive system.

🚀 Features
1️⃣ AI Chatbot (Groq LLaMA-3.1)

Detects booking intent

Collects user details conversationally

Uses short-term memory

Validates email, date, time

Summarizes & confirms before saving

Prevents invalid inputs

Optional voice output using gTTS

2️⃣ Booking Flow

The chatbot collects:

Name

Email

Phone

Pickup Type

Preferred Date

Preferred Time

Then:

Shows summary

Asks for confirmation

Stores in database

Sends confirmation email

Plays optional voice output

3️⃣ RAG – PDF Question Answering

Upload multiple PDFs

Extract text using pdfplumber

Chunk & embed using Sentence-Transformers

Store embeddings in FAISS

Retrieve most relevant chunks

Use LLaMA model to generate answers with context

Perfect for multi-document knowledge querying.

4️⃣ Admin Dashboard

Includes:

View all bookings

Pagination

Filter by name, date, email, type, status

Update booking status

Delete bookings

Export filtered results to CSV

5️⃣ Email Confirmation

Sent after booking via SMTP.

Includes:

User’s name

Booking ID

Pickup type

Date & Time

Support instructions

6️⃣ Voice Support (TTS)

Uses Google gTTS (free, no API key needed)

Converts chatbot replies to audio

Toggle option in sidebar

7️⃣ Web Search Tool (Optional)

Used when:

RAG has no answer

User explicitly asks web-related questions

Uses DuckDuckGo Instant API (free, keyless).

🧩 Tech Stack
Component	Technology
Frontend	Streamlit
Backend	Python
LLM	Groq LLaMA-3.1
RAG	FAISS + Sentence Transformers
Email	SMTP
TTS	gTTS
PDF Parsing	pdfplumber
Database	SQLite (SQLAlchemy ORM)
Web Search	DuckDuckGo API
📁 Project Structure
ecopickup/
│── app/
│   ├── main.py              # Streamlit entry point
│   ├── chat_logic.py        # Intent detection + conversational logic
│   ├── booking_flow.py      # Slot filling + confirmation
│   ├── rag_pipeline.py      # PDF ingestion + embeddings + FAISS
│   ├── tools.py             # DB save, SMTP, RAG tool, TTS, Web search
│   ├── admin_dashboard.py   # Admin panel
│── db/
│   ├── database.py          # SQLite setup
│   ├── models.py            # SQLAlchemy ORM
│── docs/                    # Sample PDFs + diagrams
│── requirements.txt         # Required dependencies
│── README.md                # Documentation
│── .streamlit/
│       └── secrets.toml     # (NOT included in repo)

🔧 Installation Instructions
1️⃣ Clone the Repository
git clone https://github.com/nandana1318biju/EcoPickup-AI-Booking-Assistant.git
cd EcoPickup-AI-Booking-Assistant

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Configure Secrets (Streamlit Cloud)

In Streamlit → Settings → Secrets:

[grop]
api_key = "YOUR_GROQ_KEY"

[smtp]
host = "smtp.gmail.com"
port = 587
user = "YOUR_EMAIL"
pass = "YOUR_APP_PASSWORD"

4️⃣ Run Locally
streamlit run app/main.py

🌍 Deployment (Streamlit Cloud)

Push project to GitHub

Create new Streamlit Cloud app

Add requirements.txt

Add secrets under Settings → Secrets

Deploy & verify the public link

🎯 Project Use Case

EcoPickup modernizes waste collection by:

Allowing users to schedule eco-friendly waste pickups

Answering sustainability and waste management questions

Helping waste companies automate bookings

Providing admins with complete operational tools

Can be extended to:

Municipal waste management

College hostel waste tracking

Corporate waste automation

Research labs (microplastic sample pickups)

👩‍💻 Author

Nandana Biju
MSc AI & ML — Christ University
AI/ML Developer • Conversational AI • RAG Systems • NLP
