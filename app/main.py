# MUST be first
import streamlit as st
st.set_page_config(page_title="EcoPickup", layout="wide")

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from db.database import init_db
from app.chat_logic import init_chat_state, handle_message
from app.tools import rag_ingest_files, web_search_tool_duckduckgo, text_to_speech

# Init DB + chat
init_db()
init_chat_state()

# ------------ SIDEBAR ------------
with st.sidebar:
    st.header("🔐 Admin Panel")
    if st.button("Go to Admin Login"):
        st.switch_page("pages/1_Admin_Login.py")

    st.markdown("---")
    st.subheader("🌐 Web Search Tool")
    q = st.text_input("Search")
    if st.button("Search"):
        if q:
            st.write(web_search_tool_duckduckgo(q))

    st.markdown("---")
    st.subheader("🔊 Voice Output")
    if "tts" not in st.session_state:
        st.session_state["tts"] = True
    st.session_state["tts"] = st.checkbox("Enable TTS", value=True)

# ------------ PDF Upload ------------
st.subheader("📄 Upload PDFs")
files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)
if files:
    res = rag_ingest_files(files)
    if res["success"]:
        st.success(f"Indexed {res['added_chunks']} chunks.")
    else:
        st.error(res["message"])

# ------------ Chat UI ------------
st.title("EcoPickup – AI Waste Pickup Assistant")

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        if msg.get("is_audio"):
            st.markdown(msg["content"], unsafe_allow_html=True)
        else:
            st.write(msg["content"])

user_input = st.chat_input("Ask something...")
if user_input:

    st.session_state["messages"].append({
        "role": "user",
        "content": user_input
    })

    reply = handle_message(user_input)

    st.session_state["messages"].append({
        "role": "assistant",
        "content": reply
    })

    # TTS
    if st.session_state["tts"]:
        audio_html = text_to_speech(reply)
        st.session_state["messages"].append({
            "role": "assistant",
            "content": audio_html,
            "is_audio": True
        })

    st.rerun()


