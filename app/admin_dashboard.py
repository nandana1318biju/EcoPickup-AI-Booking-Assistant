# app/admin_dashboard.py

import streamlit as st
import pandas as pd
import datetime
import io

from db.database import SessionLocal
from db.models import Booking, Customer
from sqlalchemy.orm import joinedload
from sqlalchemy import and_


# -----------------------------------------------------------
# 🎯 Fetch bookings with filters
# -----------------------------------------------------------
def fetch_bookings(filters: dict):
    db = SessionLocal()
    try:
        q = db.query(Booking).options(joinedload(Booking.customer))
        conditions = []

        # FILTER: Name
        if filters.get("name"):
            name_like = f"%{filters['name'].lower()}%"
            q = q.join(Customer)
            conditions.append(Customer.name.ilike(name_like))

        # FILTER: Email
        if filters.get("email"):
            email_like = f"%{filters['email'].lower()}%"
            if "Customer" not in [m.class_.__name__ for m in q.column_descriptions]:
                q = q.join(Customer)
            conditions.append(Customer.email.ilike(email_like))

        # FILTER: Pickup type
        if filters.get("pickup_type"):
            conditions.append(Booking.booking_type == filters["pickup_type"])

        # FILTER: Status
        if filters.get("status"):
            conditions.append(Booking.status == filters["status"])

        # FILTER: Date from
        if filters.get("date_from"):
            conditions.append(Booking.date >= filters["date_from"])

        # FILTER: Date to
        if filters.get("date_to"):
            conditions.append(Booking.date <= filters["date_to"])

        # APPLY FILTERS
        if conditions:
            q = q.filter(and_(*conditions))

        q = q.order_by(Booking.created_at.desc())
        return q.all()

    finally:
        db.close()


# -----------------------------------------------------------
# 📊 Convert bookings to pandas dataframe
# -----------------------------------------------------------
def bookings_to_dataframe(bookings):
    rows = []
    db = SessionLocal()

    try:
        for b in bookings:
            cust = db.query(Customer).filter(Customer.customer_id == b.customer_id).first()
            rows.append({
                "Booking ID": b.id,
                "Name": cust.name if cust else "",
                "Email": cust.email if cust else "",
                "Phone": cust.phone if cust else "",
                "Pickup Type": b.booking_type,
                "Date": b.date,
                "Time": b.time,
                "Status": b.status,
                "Created At": b.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        return pd.DataFrame(rows)
    finally:
        db.close()


# -----------------------------------------------------------
# 🟦 Status badge for table rows
# -----------------------------------------------------------
def colored_status(status):
    colors = {
        "pending": "orange",
        "confirmed": "green",
        "completed": "blue",
        "cancelled": "red"
    }
    color = colors.get(status, "gray")
    return f"<span style='color:{color};font-weight:bold'>{status}</span>"


# -----------------------------------------------------------
# 🧭 MAIN ADMIN DASHBOARD UI
# -----------------------------------------------------------
def render_admin_dashboard():
    st.title("🔐 Admin Dashboard — EcoPickup")
    st.write("Manage all customer bookings here.")

    # -----------------------------------------------------------
    # 🔍 FILTERS PANEL
    # -----------------------------------------------------------
    with st.expander("Filters", expanded=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            name_filter = st.text_input("Name contains")
            email_filter = st.text_input("Email contains")

        with col2:
            date_from = st.date_input("From date", value=None)
            date_to = st.date_input("To date", value=None)

        with col3:
            pickup_type = st.selectbox(
                "Pickup Type",
                ["", "organic", "plastic", "paper", "glass", "ewaste", "mixed", "microplastic_sample"]
            )
            status = st.selectbox(
                "Status",
                ["", "pending", "confirmed", "completed", "cancelled"]
            )

        # Convert date to string
        df_str = date_from.strftime("%Y-%m-%d") if isinstance(date_from, datetime.date) else None
        dt_str = date_to.strftime("%Y-%m-%d") if isinstance(date_to, datetime.date) else None

        if st.button("Apply Filters"):
            st.session_state["admin_filters"] = {
                "name": name_filter or None,
                "email": email_filter or None,
                "date_from": df_str,
                "date_to": dt_str,
                "pickup_type": pickup_type or None,
                "status": status or None,
            }

        if st.button("Clear Filters"):
            st.session_state.pop("admin_filters", None)
            st.rerun()

    filters = st.session_state.get("admin_filters", {})

    # -----------------------------------------------------------
    # 📚 FETCH BOOKINGS
    # -----------------------------------------------------------
    try:
        bookings = fetch_bookings(filters)
    except Exception as e:
        st.error(f"Error loading bookings: {e}")
        return

    df = bookings_to_dataframe(bookings)

    # COLOR STATUS BADGE
    if not df.empty:
        df["Status"] = df["Status"].apply(colored_status)
        st.markdown(
            """
            <style>
            td span { font-size: 14px; }
            </style>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------------
    # 📄 RESULTS TABLE + PAGINATION
    # -----------------------------------------------------------
    per_page = st.number_input("Rows per page", min_value=5, max_value=100, value=10)
    total = len(df)
    page = st.session_state.get("admin_page", 1)
    max_page = max(1, (total + per_page - 1) // per_page)

    # Pagination
    colA, colB, colC = st.columns([1, 2, 1])

    with colA:
        if st.button("Previous") and page > 1:
            page -= 1
            st.session_state["admin_page"] = page
            st.rerun()

    with colB:
        st.write(f"Page {page} of {max_page}")

    with colC:
        if st.button("Next") and page < max_page:
            page += 1
            st.session_state["admin_page"] = page
            st.rerun()

    # Paginated results
    start = (page - 1) * per_page
    end = start + per_page
    page_df = df.iloc[start:end] if not df.empty else df

    st.subheader(f"All Bookings ({total})")

    if df.empty:
        st.info("No bookings match your filters.")
    else:
        st.write(page_df.to_html(escape=False), unsafe_allow_html=True)

        # EXPORT CSV
        csv_buffer = io.StringIO()
        page_df.to_csv(csv_buffer, index=False)
        st.download_button(
            "Download CSV (current page)",
            csv_buffer.getvalue(),
            file_name="ecopickup_bookings.csv",
            mime="text/csv"
        )

    # -----------------------------------------------------------
    # ✏ MANAGE BOOKING (EDIT / DELETE)
    # -----------------------------------------------------------
    st.subheader("✏ Manage a Booking")

    booking_id = st.number_input("Enter Booking ID", min_value=0, step=1)

    if booking_id:
        db = SessionLocal()
        try:
            booking = db.query(Booking).filter(Booking.id == booking_id).first()
            if not booking:
                st.error("Booking not found.")
                return

            cust = db.query(Customer).filter(Customer.customer_id == booking.customer_id).first()

            st.markdown("### Booking Details")
            st.write(f"**Name:** {cust.name}")
            st.write(f"**Email:** {cust.email}")
            st.write(f"**Phone:** {cust.phone}")
            st.write(f"**Pickup Type:** {booking.booking_type}")
            st.write(f"**Date:** {booking.date}")
            st.write(f"**Time:** {booking.time}")
            st.write(f"**Status:** {booking.status}")

            # --------------------------
            # STATUS UPDATE
            # --------------------------
            new_status = st.selectbox(
                "Change status",
                ["pending", "confirmed", "completed", "cancelled"],
                index=["pending", "confirmed", "completed", "cancelled"].index(booking.status)
            )

            if st.button("Update Status"):
                booking.status = new_status
                db.commit()
                st.success("Status updated successfully.")
                st.rerun()

            # --------------------------
            # SAFE DELETE FLOW
            # --------------------------
            st.warning("Danger zone: Delete this booking")

            if st.button("Delete Booking"):
                st.session_state["delete_mode"] = True

            if st.session_state.get("delete_mode"):
                st.error("⚠ Are you sure you want to delete this booking permanently?")
                confirm = st.checkbox("Yes, permanently delete this booking")

                if st.button("Confirm Delete"):
                    if confirm:
                        db.delete(booking)
                        db.commit()
                        st.success("Booking deleted permanently.")
                        st.session_state["delete_mode"] = False
                        st.rerun()
                    else:
                        st.warning("Please tick the confirmation box.")

                if st.button("Cancel Delete"):
                    st.session_state["delete_mode"] = False

        finally:
            db.close()
