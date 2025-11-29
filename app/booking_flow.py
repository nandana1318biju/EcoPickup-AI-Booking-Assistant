import streamlit as st
import re
from datetime import datetime
from app.tools import save_booking_to_db, send_confirmation_email

# ---------------- REQUIRED SLOTS ------------------

REQUIRED_SLOTS = ["name", "email", "phone", "pickup_type", "date", "time"]

PICKUP_TYPES = [
    "organic",
    "plastic",
    "paper",
    "glass",
    "ewaste",
    "mixed",
    "microplastic_sample"
]

# ==================================================
#                    VALIDATION 
# ==================================================

EMAIL_REGEX = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

def validate_email(email):
    """Strict email format validation."""
    return re.match(EMAIL_REGEX, email) is not None

def validate_phone(phone):
    return re.match(r'^[\d\+\-\s]{7,15}$', phone) is not None

def validate_date(date_str):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        return d >= datetime.now().date()
    except:
        return False

def validate_time(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except:
        return False


# ==================================================
#                BOOKING FLOW HANDLER
# ==================================================

def process_booking_message(user_input):

    if "current_booking" not in st.session_state:
        st.session_state["current_booking"] = {}

    if "current_slot" not in st.session_state:
        st.session_state["current_slot"] = None

    booking = st.session_state["current_booking"]

    # If a slot question is already asked → treat the reply as answer
    if st.session_state["current_slot"] is not None:
        return save_slot_and_continue(user_input)

    # Otherwise → find the next missing field
    for slot in REQUIRED_SLOTS:
        if slot not in booking:
            st.session_state["current_slot"] = slot
            return generate_question(slot)

    # If all fields collected → show summary for approval
    return summarize_before_confirmation()


def generate_question(slot):
    questions = {
        "name": "Sure! What's your full name?",
        "email": "What's your email address?",
        "phone": "Your phone number?",
        "pickup_type": f"What type of pickup do you want? ({', '.join(PICKUP_TYPES)})",
        "date": "What date do you prefer? (YYYY-MM-DD)",
        "time": "At what time? (HH:MM)",
    }
    return questions.get(slot)


# ==================================================
#            SAVE SLOTS + VALIDATION
# ==================================================

def save_slot_and_continue(answer):

    slot = st.session_state["current_slot"]
    booking = st.session_state["current_booking"]
    value = answer.strip()

    # ---------------- VALIDATION CHECKS ----------------

    if slot == "email":
        if not validate_email(value):
            return "❌ Invalid email format. Please enter something like **name@example.com**."

    elif slot == "phone":
        if not validate_phone(value):
            return "❌ Invalid phone number. Please try again."

    elif slot == "date":
        if not validate_date(value):
            return "❌ Invalid date. Please use **YYYY-MM-DD**, and ensure it's today or later."

    elif slot == "time":
        if not validate_time(value):
            return "❌ Invalid time. Please use **HH:MM** format."

    elif slot == "pickup_type":
        if value.lower() not in PICKUP_TYPES:
            return f"❌ Invalid type. Choose one of: **{', '.join(PICKUP_TYPES)}**."

    # Save the validated slot
    booking[slot] = value
    st.session_state["current_slot"] = None

    # Continue flow
    return process_booking_message("")


# ==================================================
#              SUMMARY BEFORE CONFIRMATION
# ==================================================

def summarize_before_confirmation():
    booking = st.session_state["current_booking"]

    summary = (
        "📦 **Please confirm your EcoPickup booking:**\n\n"
        f"**Name:** {booking['name']}\n"
        f"**Email:** {booking['email']}\n"
        f"**Phone:** {booking['phone']}\n"
        f"**Pickup Type:** {booking['pickup_type']}\n"
        f"**Date:** {booking['date']}\n"
        f"**Time:** {booking['time']}\n\n"
        "Type **yes** to confirm or **no** to cancel."
    )

    st.session_state["awaiting_confirmation"] = True
    return summary


# ==================================================
#                CONFIRMATION HANDLER
# ==================================================

def handle_confirmation(user_input):

    msg = user_input.lower().strip()
    booking = st.session_state["current_booking"]

    # ------------------ CONFIRM ---------------------
    if msg == "yes":
        result = save_booking_to_db(booking)

        st.session_state["awaiting_confirmation"] = False
        st.session_state["current_slot"] = None
        st.session_state["current_booking"] = {}

        if not result["success"]:
            return f"❌ Error saving booking: {result['error']}"

        booking_id = result["booking_id"]

        # ------------------ EMAIL CONTENT --------------------
        subject = f"EcoPickup Booking Confirmation #{booking_id}"

        body = (
            f"Hello {booking['name']},\n\n"
            f"Your booking with EcoPickup has been successfully confirmed. 🌱\n\n"
            f"Here are your booking details:\n"
            f"--------------------------------------------\n"
            f"📌 Booking ID: {booking_id}\n"
            f"📦 Pickup Type: {booking['pickup_type'].title()}\n"
            f"📅 Date: {booking['date']}\n"
            f"⏰ Time: {booking['time']}\n"
            f"--------------------------------------------\n\n"
            f"If you need to modify or cancel this booking, simply reply to this email.\n\n"
            f"Thank you for choosing EcoPickup and supporting a cleaner planet 🌍\n\n"
            f"Best regards,\nEcoPickup Team\nhttps://www.ecopickup.com\n"
        )

        # ------------------ SEND EMAIL --------------------
        email_status = send_confirmation_email(booking["email"], subject, body)

        if not email_status["success"]:
            return (
                f"🎉 Booking Confirmed! (ID: {booking_id})\n"
                f"⚠️ However, the confirmation email could not be sent.\n"
                f"Reason: {email_status.get('error', 'Unknown error')}."
            )

        return f"🎉 Booking Confirmed! (ID: {booking_id})\n📧 Confirmation email sent."

    # ------------------ CANCEL ---------------------
    elif msg == "no":
        st.session_state["awaiting_confirmation"] = False
        st.session_state["current_slot"] = None
        st.session_state["current_booking"] = {}
        return "❌ Booking cancelled."

    # ------------------ INVALID RESPONSE ---------------------
    else:
        return "Please type **yes** or **no**."
