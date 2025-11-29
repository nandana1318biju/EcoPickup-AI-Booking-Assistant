# app/chat_logic.py

import streamlit as st
from app.booking_flow import process_booking_message, handle_confirmation
from app.tools import rag_tool, llm_complete


# ------------------------------------------------------------
# INITIALIZE CHAT STATE
# ------------------------------------------------------------
def init_chat_state():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if "current_booking" not in st.session_state:
        st.session_state["current_booking"] = {}

    if "current_slot" not in st.session_state:
        st.session_state["current_slot"] = None

    if "awaiting_confirmation" not in st.session_state:
        st.session_state["awaiting_confirmation"] = False


# ------------------------------------------------------------
# INTENT DETECTION
# ------------------------------------------------------------
def detect_intent(message):
    msg = message.lower().strip()

    # 🔵 RAG keywords (knowledge-based queries)
    rag_keywords = [
        "pdf", "explain", "define", "summarize", "describe",
        "according", "examples of", "what are", "what is",
        "list", "give me", "tell me about"
    ]

    # 🟢 Booking keywords (action)
    booking_keywords = ["book", "pickup", "schedule", "appointment"]

    # 1️⃣ If user asks a question (ends with "?") → assume RAG
    if msg.endswith("?"):
        return "rag"

    # 2️⃣ Keyword-based RAG detection
    if any(k in msg for k in rag_keywords):
        return "rag"

    # 3️⃣ Booking intent
    if any(k in msg for k in booking_keywords):
        return "booking"

    # 4️⃣ Otherwise general
    return "general"


# ------------------------------------------------------------
# MAIN CHAT HANDLER
# ------------------------------------------------------------
def handle_message(user_input):

    # 1️⃣ Still awaiting YES/NO for booking confirmation
    if st.session_state["awaiting_confirmation"]:
        return handle_confirmation(user_input)

    # 2️⃣ If booking flow already started → continue it
    if (
        st.session_state["current_slot"] is not None
        or len(st.session_state.get("current_booking", {})) > 0
    ):
        return process_booking_message(user_input)

    # 3️⃣ Detect the intent
    intent = detect_intent(user_input)

    # --------------------------------------------------------
    # BOOKING MESSAGE
    # --------------------------------------------------------
    if intent == "booking":
        return process_booking_message(user_input)

    # --------------------------------------------------------
    # RAG OR GENERAL QUESTION
    # --------------------------------------------------------
    if intent == "rag":

        # Try RAG (vector search)
        res = rag_tool(user_input)

        # If no PDF indexed → pure LLaMA response
        if not res["success"]:
            return llm_complete(user_input)

        # PDF + LLaMA answer
        answer = res["answer"]
        sources = res.get("sources", [])

        if sources:
            unique_sources = {s["source"] for s in sources}
            answer += "\n\n📚 **Sources:** " + ", ".join(unique_sources)

        return answer

    # --------------------------------------------------------
    # GENERAL MESSAGE → LLaMA RESPONSE
    # --------------------------------------------------------
    return llm_complete(
        "You are EcoPickup AI, a friendly waste-management assistant. "
        "User message: " + user_input
    )

