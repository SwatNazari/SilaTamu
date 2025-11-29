import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Homestay Booking", page_icon="🏡")

st.title("🏡 Homestay Booking System (1 Room Only)")

PRICE_PER_NIGHT = 150  # Set your rate here


# ============================================================
# Load existing bookings
# ============================================================
def load_bookings():
    try:
        return pd.read_csv("booking_list.csv", parse_dates=["Check-In", "Check-Out"])
    except:
        return pd.DataFrame(columns=["Name", "Phone", "Check-In", "Check-Out", "Nights", "Total Price"])


bookings = load_bookings()


# ============================================================
# Guest info
# ============================================================
st.header("Guest Information")
name = st.text_input("Full Name")
phone = st.text_input("Phone Number (WhatsApp)")

st.header("Booking Details")
check_in = st.date_input("Check-In Date", min_value=date.today())
check_out = st.date_input("Check-Out Date", min_value=check_in)


# ============================================================
# Check availability (1 room only)
# ============================================================
def is_available(start, end):
    """Check if room is available for selected date range"""
    for _, row in bookings.iterrows():
        booked_start = row["Check-In"].date()
        booked_end = row["Check-Out"].date()

        # Overlap condition
        if start < booked_end and end > booked_start:
            return False
    return True


# Nights calculation
if check_out > check_in:
    nights = (check_out - check_in).days
else:
    nights = 0

total_price = nights * PRICE_PER_NIGHT

st.write(f"**Price per night:** RM {PRICE_PER_NIGHT}")
st.write(f"**Total nights:** {nights}")
st.write(f"### Total Price: RM {total_price}")


# ============================================================
# Confirm booking
# ============================================================
if st.button("Confirm Booking"):

    if name == "" or phone == "" or nights == 0:
        st.error("Please complete all fields properly.")

    elif not is_available(check_in, check_out):
        st.error("❌ Room is already booked for these dates. Please choose another date.")

    else:
        # Save booking
        new_booking = pd.DataFrame([{
            "Name": name,
            "Phone": phone,
            "Check-In": check_in,
            "Check-Out": check_out,
            "Nights": nights,
            "Total Price": total_price
        }])

        all_bookings = pd.concat([bookings, new_booking], ignore_index=True)
        all_bookings.to_csv("booking_list.csv", index=False)

        st.success("✅ Booking confirmed!")

        # WhatsApp Message
        msg = (
            f"Homestay Booking Confirmation:%0A"
            f"Name: {name}%0A"
            f"Phone: {phone}%0A"
            f"Check In: {check_in}%0A"
            f"Check Out: {check_out}%0A"
            f"Nights: {nights}%0A"
            f"Total Price: RM {total_price}"
        )
        wa_url = f"https://wa.me/{60193637573}?text={msg}"

        st.markdown(f"[Send via WhatsApp]({wa_url})")


# ============================================================
# Show bookings
# ============================================================
st.header("📘 Booking Records")
if len(bookings) > 0:
    st.dataframe(bookings)
else:
    st.info("No bookings yet.")