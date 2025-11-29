🌱 EcoPickup — AI Waste Pickup Booking Assistant

An end-to-end AI-powered application for waste pickup scheduling, PDF-based Q&A using RAG,
voice-enabled chatbot (TTS), email notifications, and a complete Admin Dashboard.

⭐ Overview

EcoPickup is an AI chatbot designed to make waste pickup services smart, fast, and automated.

Users can:

Book organic, plastic, paper, glass, e-waste, mixed waste, or microplastic sample pickups

Ask questions from uploaded PDFs using RAG

Receive voice-generated AI replies (TTS)

Receive email confirmations

View and modify bookings using an Admin Portal

This project demonstrates skills in:

Conversational AI

Retrieval Augmented Generation (RAG)

Database design

Tool calling (DB, Email, RAG, Search)

Streamlit front-end engineering

Deployment on Streamlit Cloud

🔐 Admin Login Details

To access the Admin Dashboard:

Admin Password: admin123


These credentials are safe—admin panel is isolated and does not access any sensitive system.

🚀 Features
1️⃣ AI Chatbot (Groq LLaMA-3.1)

Detects booking intent

Collects user details conversationally

Uses short-term memory

Validates email, date & time

Summarizes and confirms before saving

Prevents invalid inputs

Replies with optional voice output (gTTS)

2️⃣ Booking Flow

The chatbot collects:

Name

Email

Phone

Pickup Type

Preferred Date

Preferred Time

Then:

✔ Shows summary
✔ Asks for confirmation
✔ Stores in database
✔ Sends confirmation email
✔ Produces voice output

3️⃣ RAG — PDF Question Answering

Upload any number of PDFs

Extract text using pdfplumber

Chunk + embed using Sentence Transformers

Store embeddings in FAISS

Retrieve relevant text

AI answers using LLaMA model + retrieved context

Perfect for multi-document knowledge querying.

4️⃣ Admin Dashboard

Includes:

View all bookings

Pagination

Filter by name, date, email, type, status

Update booking status

Delete bookings

Export filtered bookings to CSV

5️⃣ Email Confirmation

Sent via SMTP after booking.

Includes:

User’s name

Booking ID

Date & Time

Pickup type

EcoPickup website

Support instructions

6️⃣ Voice Support (TTS)

Uses Google gTTS (free, no API key needed)

Converts every chatbot reply into audio

Toggle available in sidebar

7️⃣ Web Search Tool (Optional)

Uses DuckDuckGo Instant API when:

User asks something not found in RAG

User explicitly requests general web information

🧩 Tech Stack
Component	Technology
Frontend	Streamlit
Backend	Python
LLM	Groq LLaMA-3.1 via Groq API
RAG	FAISS + Sentence Transformers
Email	SMTP
TTS	gTTS
PDF Parsing	pdfplumber
Database	SQLite (SQLAlchemy ORM)
Search Tool	DuckDuckGo API
📁 Project Structure
ecopickup/
│── app/
│   ├── main.py              # Streamlit entry point
│   ├── chat_logic.py        # Intent detection + conversational logic
│   ├── booking_flow.py      # Slot filling + confirmation
│   ├── rag_pipeline.py      # PDF ingestion + embeddings + FAISS
│   ├── tools.py             # DB save, SMTP, RAG tool, TTS, Web search
│   ├── admin_dashboard.py   # Admin management panel
│── db/
│   ├── database.py          # SQLite setup
│   ├── models.py            # SQLAlchemy ORM
│── docs/                    # Sample PDFs + diagrams
│── README.md                # Documentation
│── requirements.txt         # Python dependencies
│── .streamlit/
│       └── secrets.toml     # (NOT included in repo — only on deployment)

🔧 Installation Instructions
1️⃣ Clone the Repository
git clone https://github.com/nandana1318biju/EcoPickup-AI-Booking-Assistant.git
cd EcoPickup-AI-Booking-Assistant

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Configure Secrets (Streamlit Cloud)

In Streamlit Cloud → Secrets:

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

Deploy and verify public link works

🎯 Project Use Case

EcoPickup modernizes waste collection by:

Allowing users to schedule eco-friendly waste pickups

Answering sustainability and waste management questions

Helping waste management companies automate bookings

Providing admin tools to manage operations

It can be extended to:
♻ Municipal waste management
♻ College hostel waste tracking
♻ Company waste pickup automation
♻ Laboratory microplastic sample collection

👩‍💻 Author

Nandana Biju
MSc AI & ML – Christ University
AI/ML Developer • Conversational AI • RAG Systems • NLP
