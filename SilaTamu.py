import streamlit as st
import json
from datetime import datetime
import webbrowser
import urllib.parse

# ---------------------- Function: Print to Console ----------------------
def printOrder(CustomerName, TableNum, OrderItem, TotalHarga):
    print("-------------------------------------")
    print(f"{CustomerName.upper()} [Meja Nombor: {TableNum} | Jumlah: RM{TotalHarga:.2f}]")
    print("-------------------------------------")
    for item, details in OrderItem.items():
        subtotal = details["qty"] * details["price"]
        print(f"{item} x {details['qty']} = RM{subtotal:.2f}")
        if details['note']:
            print(f"  Nota: {details['note']}")
    print("-------------------------------------")

# ---------------------- Function: Save Order to Text File ----------------------
def send_order_to_whatsapp(CustomerName, TableNum, OrderItem, TotalHarga, phone_number="60193637573"):
    message_lines = [
        "📦 *Pesanan Baru Diterima*",
        "=====================================",
        f"👤 *Nama Pelanggan:* {CustomerName.upper()}",
        f"🪑 *Nombor Meja:* {TableNum}",
        f"🕒 *Masa:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "-------------------------------------",
    ]
    for item, details in OrderItem.items():
        qty = details["qty"]
        price = details["price"]
        subtotal = qty * price
        message_lines.append(f"{item} x {qty} = RM{subtotal:.2f}")
        if details.get("note"):
            message_lines.append(f"  Nota: {details['note']}")
    message_lines.extend([
        "-------------------------------------",
        f"💵 *Jumlah:* RM{TotalHarga:.2f}",
        "=====================================",
    ])
    full_message = "\n".join(message_lines)
    encoded_message = urllib.parse.quote(full_message)
    # Generate WhatsApp link
    whatsapp_url = f"https://wa.me/{phone_number}?text={encoded_message}"
    # Show link on Streamlit (phone users can tap this to send)
    orderconfirmation = st.markdown(f"[📲 Klik disini untuk mengesahkan pesanan]({whatsapp_url})", unsafe_allow_html=True)
# ---------------------- Load Menu ----------------------
with open('SilaTamu-Menu.json') as myMenu:
    menu = json.load(myMenu)

# ---------------------- UI Layout ----------------------
st.set_page_config(page_title="SilaTamu Ordering", page_icon="🍽️")
st.title("🍽️ Selamat Datang ke SilaTamu!")
st.markdown("Pilih menu kegemaran anda dan buat pesanan anda sekarang. 😊")

# Customer name and table number
col1, col2 = st.columns([2, 1])
with col1:
    CustomerName = st.text_input("🧑‍🍳 Nama Pelanggan")
with col2:
    selected_table = st.selectbox("🪑 Nombor Meja", list(range(1, 11)))
# ---------------------- Tabs per Category ----------------------
tabs = st.tabs(list(menu.keys()))
order_cart = {}
# ---------------------- Order Summary ----------------------
st.markdown("---")
st.subheader("🧾 Ringkasan Pesanan")

if order_cart:
    total = 0
    for item, details in order_cart.items():
        subtotal = details["qty"] * details["price"]
        total += subtotal
        st.write(f"🔹 {item} x {details['qty']} = RM{subtotal:.2f}")
        if details['note']:
            st.write(f"   📝 Nota: {details['note']}")
    st.markdown(f"## 💰 Jumlah Keseluruhan: RM{total:.2f}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Hantar Pesanan"):
            if CustomerName.strip():
                printOrder(CustomerName, selected_table, order_cart, total)
                whatsapp_url = send_order_to_whatsapp(CustomerName, selected_table, order_cart, total)
            else:
                st.warning("⚠️ Sila masukkan nama pelanggan.")
else:
    st.info("🛒 Tiada item dalam pesanan. Sila pilih dari menu di atas.")
