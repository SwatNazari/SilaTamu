import streamlit as st
import pandas as pd
from datetime import datetime
import webbrowser

st.set_page_config(page_title="Homestay Booking System", page_icon="🏡", layout="centered")

st.title("🏡 Homestay Booking System")

# ============================================================
# ROOM PACKAGES
# ============================================================
room_data = {
    "Standard Room": 120,
    "Deluxe Room": 180,
    "Family Suite": 250,
    "Villa": 400,
}

# ============================================================
# USER INPUT FORM
# ============================================================
st.header("Guest Information")

name = st.text_input("Full Name")
phone = st.text_input("Phone Number (WhatsApp)")

st.header("Booking Details")

room = st.selectbox("Select Room Type", list(room_data.keys()))
price_per_night = room_data[room]

check_in = st.date_input("Check-In Date")
check_out = st.date_input("Check-Out Date")

# Nights calculation
if check_out > check_in:
    nights = (check_out - check_in).days
else:
    nights = 0

total_price = nights * price_per_night

st.write(f"**Price per night:** RM {price_per_night}")
st.write(f"**Total nights:** {nights}")
st.write(f"### Total Price: **RM {total_price}**")


# ============================================================
# SAVE BOOKING
# ============================================================
if st.button("Confirm Booking"):
    if name == "" or phone == "" or nights == 0:
        st.error("Please complete all fields properly.")
    else:
        booking = {
            "Name": name,
            "Phone": phone,
            "Room": room,
            "Check-In": check_in.strftime("%Y-%m-%d"),
            "Check-Out": check_out.strftime("%Y-%m-%d"),
            "Nights": nights,
            "Total Price": total_price
        }

        # Save to CSV
        df = pd.DataFrame([booking])

        try:
            existing = pd.read_csv("booking_list.csv")
            df = pd.concat([existing, df], ignore_index=True)
        except:
            pass

        df.to_csv("booking_list.csv", index=False)

        st.success("Booking Confirmed! Saved successfully.")

        # WhatsApp link auto-format
        whatsapp_msg = (
            f"Hello, I would like to confirm my booking:%0A"
            f"Name: {name}%0A"
            f"Phone: {phone}%0A"
            f"Room: {room}%0A"
            f"Check-In: {booking['Check-In']}%0A"
            f"Check-Out: {booking['Check-Out']}%0A"
            f"Nights: {nights}%0A"
            f"Total Price: RM {total_price}"
        )

        wa_url = f"https://wa.me/{phone}?text={whatsapp_msg}"

        st.markdown(f"[Send Booking Details via WhatsApp]({wa_url})")


# ============================================================
# RESET BUTTON
# ============================================================
if st.button("Reset Form"):
    st.experimental_rerun()


# ============================================================
# VIEW SAVED BOOKINGS
# ============================================================
st.header("📘 Booking Records")

try:
    history = pd.read_csv("booking_list.csv")
    st.dataframe(history)
except:
    st.info("No bookings yet.")