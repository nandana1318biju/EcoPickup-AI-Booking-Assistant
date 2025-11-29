import streamlit as st
from app.admin_dashboard import render_admin_dashboard

st.set_page_config(page_title="EcoPickup Admin", layout="wide")

ADMIN_PASSWORD = "admin123"

st.title("🔐 Admin Login")

if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

if not st.session_state["admin_logged_in"]:
    pwd = st.text_input("Enter admin password", type="password")
    if st.button("Login"):
        if pwd == ADMIN_PASSWORD:
            st.session_state["admin_logged_in"] = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Incorrect password.")
else:
    st.success("Welcome, Admin!")
    render_admin_dashboard()
