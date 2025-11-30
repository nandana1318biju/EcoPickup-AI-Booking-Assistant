# 🌱 EcoPickup — AI Waste Pickup Booking Assistant

An end-to-end AI-powered application for:

- Smart waste pickup scheduling  
- PDF-based Q&A using RAG  
- AI chatbot powered by Groq LLaMA  
- Voice-enabled replies (TTS)  
- Email confirmations  
- Complete Admin Dashboard  
- Deployed on Streamlit Cloud  

---

## ⭐ Overview

**EcoPickup** modernizes waste pickup services using AI.

Users can:

- Book **organic**, **plastic**, **paper**, **glass**, **e-waste**, **mixed waste**, or **microplastic sample** pickups  
- Ask questions from **uploaded PDFs** using RAG  
- Listen to **AI-generated voice replies**  
- Receive **email confirmation**  
- Admin can **view, update, delete, and export bookings**

This project demonstrates:

- Conversational AI  
- Retrieval Augmented Generation (RAG)  
- Database design  
- Tool calling: DB, Email, RAG, Search  
- Streamlit front-end engineering  
- Full deployment workflow  

---

## 🔐 Admin Login Details

To access the admin dashboard:

```
Admin Password: admin123
```


*(Safe because admin panel is isolated and not system-critical.)*

---

## 🚀 Features

### **1️⃣ AI Chatbot (Groq LLaMA-3.1)**
- Detects booking intent  
- Conversationally collects user details  
- Validates email, date, time  
- Uses short-term memory  
- Summarizes booking before submitting  
- Integrates RAG for knowledge Q&A  
- Replies with optional **voice output (gTTS)**  

---

### **2️⃣ Booking Flow**

The assistant collects:

- Name  
- Email  
- Phone  
- Pickup Type  
- Preferred Date  
- Preferred Time  

Then:

✔ Displays summary  
✔ Asks for confirmation  
✔ Saves booking  
✔ Sends confirmation email  
✔ Speaks out the reply (TTS)  

---

### **3️⃣ RAG — PDF Question Answering**

- Upload multiple PDFs  
- Extract text using **pdfplumber**  
- Chunk + embed using **Sentence Transformers**  
- Store embeddings in **ChromaDB**  
- Retrieve top-matching chunks  
- Answer using **Groq LLaMA model + context**

Use cases:

- Waste management manuals  
- Sustainability guidelines  
- Hazardous waste protocols  

---

### **4️⃣ Admin Dashboard**

Admin can:

- View all bookings  
- Filter by name, email, date, type, status  
- Update booking status  
- Delete bookings  
- Export data as CSV  
- Paginated display (fast & scalable)

---

### **5️⃣ Email Confirmation**

Sent automatically after booking.

Includes:

- User name  
- Booking ID  
- Pickup details  
- Support instructions  
- Contact info  

Uses SMTP with secure app passwords.

---

### **6️⃣ Voice Support (TTS)**

- Powered by **Google gTTS** (free)  
- Converts all chatbot replies into audio  
- On/Off switch in the sidebar  

---

### **7️⃣ Optional Web Search Tool**

Uses **DuckDuckGo Instant Answer API** to answer general web queries.

---

## 🧩 Tech Stack

| Component | Technology |
|----------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Database | SQLite (SQLAlchemy ORM) |
| LLM | Groq LLaMA-3.3-70B |
| RAG | ChromaDB + Sentence Transformers |
| PDF Parsing | pdfplumber |
| Email | SMTP |
| TTS | gTTS |
| Web Search | DuckDuckGo API |

---

## 📁 Project Structure

```
ecopickup/
│── app/
│ ├── main.py # Streamlit entry point
│ ├── chat_logic.py # Intent detection + conversation flow
│ ├── booking_flow.py # Slot filling + booking confirmation
│ ├── rag_pipeline.py # PDF ingestion + embeddings + ChromaDB
│ ├── tools.py # RAG, Email, DB, TTS, Web Search
│ ├── admin_dashboard.py # Admin controls
│── db/
│ ├── database.py # SQLite setup
│ ├── models.py # SQLAlchemy ORM models
│── docs/ # Sample PDFs (RAG sources)
│── requirements.txt
│── README.md
│── .streamlit/
│ └── secrets.toml # Exists in deployment only, not in repo
```


---

## 🔧 Installation Instructions

### **1️⃣ Clone Repository**

```
git clone https://github.com/nandana1318biju/EcoPickup-AI-Booking-Assistant.git

cd EcoPickup-AI-Booking-Assistant
```

### **2️⃣ Install Dependencies**
```
pip install -r requirements.txt
```


### **3️⃣ Add Secrets (Streamlit Cloud)**  
Go to **Settings → Secrets** and add:

```
[groq]
api_key = "YOUR_GROQ_KEY"

[smtp]
host = "smtp.gmail.com"
port = 587
user = "YOUR_EMAIL"
pass = "YOUR_APP_PASSWORD"
```


### **4️⃣ Run Locally**

```
streamlit run app/main.py
```


---

## 🌍 Deployment (Streamlit Cloud)

1. Push code to GitHub  
2. Create new Streamlit Cloud app  
3. Set main file as:  
```
app/main.py
```

4. Add secrets  
5. Deploy  
6. App becomes publicly accessible  

---

## 🎯 Use Cases

EcoPickup can be used for:

- Municipal waste management  
- Hostel waste collection  
- Corporate sustainability programs  
- Hazardous waste training  
- AI-driven scheduling systems  
- Microplastic research labs  

---

## 👩‍💻 Author

**Nandana Biju**  
MSc Artificial Intelligence & Machine Learning — Christ University  


