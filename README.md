🌱 EcoPickup — AI Waste Pickup Booking Assistant

An end-to-end AI-powered system for waste pickup scheduling, PDF-based RAG question answering, voice-enabled chatbot (TTS), automated email notifications, and a complete Admin Dashboard — all deployed using Streamlit Cloud.

⭐ Overview

EcoPickup is an AI chatbot that makes waste pickup services smart, fast, and fully automated.

Users can:

Book organic, plastic, paper, glass, e-waste, mixed waste, or microplastic sample pickups

Ask questions from their uploaded PDFs using RAG

Receive voice-generated replies (TTS)

Get email confirmations

Manage bookings via a built-in Admin Dashboard

This project demonstrates:

Conversational AI

Retrieval Augmented Generation (RAG)

SQL database design

Tool calling (DB, Email, RAG, Search)

Streamlit application engineering

Deployment on Streamlit Cloud

🔐 Admin Login Details

To access the Admin Dashboard:

*Admin Password*: admin123

These credentials are safe — the admin panel only controls the local SQLite demo database.

🚀 Features
1️⃣ AI Chatbot (Groq LLaMA-3.1)

Detects booking intent

Multi-turn conversational detail collection

Short-term memory

Validation for email, date, time, type

Summarizes and asks for confirmation

Stores only after explicit user approval

Optional voice output (TTS)

2️⃣ Booking Flow

The chatbot collects:

Field	Description
Name	Customer full name
Email	Valid email address
Phone	User phone number
Pickup Type	organic / plastic / paper / etc.
Preferred Date	YYYY-MM-DD
Preferred Time	HH:MM

After collecting details:

✔ Shows summary
✔ Asks for confirmation
✔ Saves to database
✔ Sends email confirmation
✔ Outputs voice reply

3️⃣ RAG — PDF Question Answering

Upload multiple PDFs

Text extraction via pdfplumber

Chunking + embedding with Sentence Transformers

Vector search using FAISS

RAG prompts with Groq LLaMA

Perfect for multi-document knowledge retrieval.

4️⃣ Admin Dashboard

Includes:

View all bookings

Pagination

Filter by name, email, date, type, status

Update status

Delete bookings

Export bookings → CSV

5️⃣ Email Confirmation

Sent via SMTP after booking.

Includes:

Name

Booking ID

Pickup type

Date & Time

Support info

EcoPickup branding

6️⃣ Voice Support (TTS)

Uses Google gTTS (free, no API key).

Converts chatbot responses into MP3

Audio player shown in chat

Can be toggled ON/OFF in sidebar

7️⃣ Web Search Tool (Optional)

Uses DuckDuckGo Instant API when:

Info is not available in PDFs

User explicitly asks for "web search" or general knowledge

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
│   ├── chat_logic.py        # Intent detection + routing
│   ├── booking_flow.py      # Slot filling + confirmation
│   ├── rag_pipeline.py      # PDF ingestion + embeddings + FAISS
│   ├── tools.py             # DB save, email, RAG, TTS, search
│   ├── admin_dashboard.py   # Admin portal
│
│── db/
│   ├── database.py          # SQLite initialization
│   ├── models.py            # SQLAlchemy models
│
│── docs/                    # Sample PDFs + diagrams
│── requirements.txt
│── README.md
│
│── .streamlit/
│       └── secrets.toml     # Not included — added only in deployment

🔧 Installation Instructions
1️⃣ Clone Repository
git clone https://github.com/nandana1318biju/EcoPickup-AI-Booking-Assistant.git
cd EcoPickup-AI-Booking-Assistant

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Configure Secrets (Streamlit Cloud)

Settings → Secrets → Paste:

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

Push code to GitHub

Create a new Streamlit Cloud app

Add requirements.txt

Add secrets under Settings → Secrets

Deploy

Share public URL

🎯 Project Use Case

EcoPickup modernizes the waste pickup process:

Eco-friendly waste scheduling

Sustainability education via PDF Q&A

Automates operations for waste companies

Admin dashboard for management

Can be extended into:

♻ Municipal waste management
♻ College hostel waste tracking
♻ Company waste automation
♻ Laboratory microplastic sampling

👩‍💻 Author

Nandana Biju
MSc AI & ML – Christ University
AI/ML Developer • Conversational AI • RAG Systems • NLP


