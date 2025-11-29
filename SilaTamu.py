import streamlit as st
import pandas as pd
from datetime import date


# ------------------------------------------------------------
# PAGE SETTINGS
# ------------------------------------------------------------
st.set_page_config(page_title="Homestay Booking", page_icon="🏡")
st.title("🏡 Homestay Booking System (1 Room Only)")


# ------------------------------------------------------------
# PRICE SETTINGS
# ------------------------------------------------------------
PRICE_PER_NIGHT = 150  # Set your homestay price here


# ------------------------------------------------------------
# LOAD EXISTING BOOKINGS (FIXED DATE PARSING)
# ------------------------------------------------------------
def load_bookings():
    try:
        df = pd.read_csv("booking_list.csv")

        # Convert string to datetime
        df["Check-In"] = pd.to_datetime(df["Check-In"])
        df["Check-Out"] = pd.to_datetime(df["Check-Out"])

        return df

    except:
        return pd.DataFrame(columns=[
            "Name", "Phone", "Check-In", "Check-Out", "Nights", "Total Price"
        ])


bookings = load_bookings()


# ------------------------------------------------------------
# CHECK AVAILABILITY (FIXED)
# ------------------------------------------------------------
def is_available(start, end):
    """Check if selected dates overlap existing bookings."""
    for _, row in bookings.iterrows():

        # Always ensure correct datetime conversion
        booked_start = pd.to_datetime(row["Check-In"]).date()
        booked_end = pd.to_datetime(row["Check-Out"]).date()

        # Overlap logic → NOT available
        if start < booked_end and end > booked_start:
            return False

    return True


# ------------------------------------------------------------
# WHATSAPP SUMMARY GENERATOR
# ------------------------------------------------------------
def generate_whatsapp_summary(name, phone, check_in, check_out, nights, total_price):
    msg = (
        f"Homestay Booking Summary:%0A"
        f"-------------------------%0A"
        f"Name: {name}%0A"
        f"Phone: {phone}%0A"
        f"Check-In: {check_in}%0A"
        f"Check-Out: {check_out}%0A"
        f"Nights: {nights}%0A"
        f"Total Price: RM {total_price}%0A"
        f"-------------------------%0A"
        f"Thank you for your booking! 😊"
    )
    return f"https://wa.me/{phone}?text={msg}"


# ------------------------------------------------------------
# USER INPUT FORM
# ------------------------------------------------------------
st.header("Guest Information")

name = st.text_input("Full Name")
phone = st.text_input("Phone Number (WhatsApp)")


st.header("Booking Details")

check_in = st.date_input("Check-In Date", min_value=date.today())
check_out = st.date_input("Check-Out Date", min_value=check_in)


# ------------------------------------------------------------
# PRICE CALCULATION
# ------------------------------------------------------------
if check_out > check_in:
    nights = (check_out - check_in).days
else:
    nights = 0

total_price = nights * PRICE_PER_NIGHT

st.write(f"**Price per night:** RM {PRICE_PER_NIGHT}")
st.write(f"**Total nights:** {nights}")
st.write(f"### Total Price: **RM {total_price}**")


# ------------------------------------------------------------
# BOOKING CONFIRMATION
# ------------------------------------------------------------
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

        st.success("✅ Booking confirmed! Booking saved successfully.")

        # Generate WhatsApp summary link
        wa_link = generate_whatsapp_summary(
            name, phone, check_in, check_out, nights, total_price
        )

        st.markdown("### 📲 Send Summary to Guest")
        st.markdown(f"[Send via WhatsApp]({wa_link})")


# ------------------------------------------------------------
# SHOW ALL BOOKINGS
# ------------------------------------------------------------
st.header("📘 Booking Records")

if len(bookings) > 0:
    st.dataframe(bookings)
else:
    st.info("No bookings yet.")