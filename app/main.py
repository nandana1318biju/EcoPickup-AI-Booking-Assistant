# ----------------------------------------------------------
# MUST BE THE FIRST STREAMLIT COMMAND
# ----------------------------------------------------------
import streamlit as st
st.set_page_config(page_title="EcoPickup", layout="wide")

# ----------------------------------------------------------
# IMPORTS (AFTER set_page_config)
# ----------------------------------------------------------
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from db.database import init_db
from app.chat_logic import init_chat_state, handle_message
from app.tools import rag_ingest_files
from app.tools import web_search_tool_duckduckgo
from app.tools import text_to_speech


# ----------------------------------------------------------
# INITIALIZE DATABASE + CHAT STATE
# ----------------------------------------------------------
init_db()
init_chat_state()


# ----------------------------------------------------------
# SIDEBAR (ADMIN + RAG + WEB SEARCH)
# ----------------------------------------------------------
with st.sidebar:
    st.header("🔐 Admin Panel")
    st.caption("Only for administrators.")

    if st.button("Go to Admin Login"):
        st.switch_page("pages/1_Admin_Login.py")

    st.markdown("---")
    st.subheader("📄 RAG Documents")
    st.caption("Upload PDFs to enable PDF-based question answering.")

    st.markdown("---")
    st.subheader("🌐 Web Search Tool (Test)")
    query = st.text_input("Enter web search query")
    if st.button("Run Web Search"):
        if query:
            res = web_search_tool_duckduckgo(query)
            st.write(res)
        else:
            st.warning("Please enter a query before running the search.")


# ----------------------------------------------------------
# RAG PDF UPLOAD SECTION
# ----------------------------------------------------------
st.subheader("📄 Upload PDFs for RAG")
uploaded = st.file_uploader(
    "Upload one or more PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded:
    res = rag_ingest_files(uploaded)
    if res["success"]:
        st.success(
            f"Indexed **{res.get('added_chunks', 0)}** document chunks. PDF search is now enabled."
        )
    else:
        st.warning(res.get("message", "No text found in PDFs."))


# ----------------------------------------------------------
# MAIN CHATBOT UI
# ----------------------------------------------------------
st.title("EcoPickup – AI Waste Pickup Assistant")

# Show previous messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        if msg.get("is_audio"):
            # render audio
            st.markdown(msg["content"], unsafe_allow_html=True)
        else:
            st.write(msg["content"])


# User input box
user_input = st.chat_input("Ask something...")
if user_input:

    # Add user message
    st.session_state["messages"].append({
        "role": "user",
        "content": user_input
    })

    # Generate bot reply (booking, rag, general, search)
    bot_reply = handle_message(user_input)

    # Add text reply first
    st.session_state["messages"].append({
        "role": "assistant",
        "content": bot_reply
    })

    # ----------------------------------------------------------
    # TTS — Convert bot reply to voice
    # ----------------------------------------------------------
    audio_html = text_to_speech(bot_reply)
    st.session_state["messages"].append({
        "role": "assistant",
        "content": audio_html,
        "is_audio": True
    })

    st.rerun()


