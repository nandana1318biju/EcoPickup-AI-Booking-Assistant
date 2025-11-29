# app/chat_logic.py

import streamlit as st
from app.booking_flow import process_booking_message, handle_confirmation
from app.tools import rag_tool

def init_chat_state():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "current_booking" not in st.session_state:
        st.session_state["current_booking"] = {}
    if "current_slot" not in st.session_state:
        st.session_state["current_slot"] = None
    if "awaiting_confirmation" not in st.session_state:
        st.session_state["awaiting_confirmation"] = False


def detect_intent(message):
    msg = message.lower().strip()

    rag_keys = ["what", "explain", "define", "pdf", "summarize", "according", "list"]
    booking_keys = ["book", "pickup", "schedule", "appointment"]

    if msg.endswith("?"):
        return "rag"
    if any(k in msg for k in rag_keys):
        return "rag"
    if any(k in msg for k in booking_keys):
        return "booking"
    return "general"


def handle_message(user_input):

    if st.session_state["awaiting_confirmation"]:
        return handle_confirmation(user_input)

    if (
        st.session_state["current_slot"] is not None
        or len(st.session_state["current_booking"]) > 0
    ):
        return process_booking_message(user_input)

    intent = detect_intent(user_input)

    if intent == "booking":
        return process_booking_message(user_input)

    elif intent == "rag":
        res = rag_tool(user_input)
        if not res["success"]:
            return "Please upload PDFs first."
        answer = res["answer"]

        sources = res.get("sources", [])
        if sources:
            src_names = {s["source"] for s in sources}
            answer += "\n\n📚 Sources: " + ", ".join(src_names)

        return answer

    else:
        return (
            "I can help you with waste pickups, scheduling, or answering questions "
            "from your uploaded PDFs. How may I assist?"
        )


