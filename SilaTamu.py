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
    return whatsapp_url

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

# ---------------------- Search Function ----------------------
search_query = st.text_input("🔍 Cari Menu", "")

# ---------------------- Tabs per Category ----------------------
tabs = st.tabs(list(menu.keys()))
order_cart = {}

# ---------------------- Menu Items with Search ----------------------
for i, category in enumerate(menu.keys()):
    with tabs[i]:
        st.header(f"📂 {category}")
        found = False
        for item in menu[category]:
            if search_query.lower() in item["name"].lower():
                found = True
                col1, col2, col3 = st.columns([1, 2, 2])
                with col1:
                    st.image(item["img"], width=100)
                with col2:
                    st.subheader(item["name"])
                    st.write(f"💵 Harga: RM{item['price']:.2f}")
                with col3:
                    qty_key = f"{category}_{item['name']}_qty"
                    note_key = f"{category}_{item['name']}_note"
                    qty = st.number_input("Kuantiti", min_value=0, step=1, key=qty_key)
                    note = st.text_input("Nota", key=note_key)

                    if qty > 0:
                        order_cart[item["name"]] = {
                            "qty": qty,
                            "price": item["price"],
                            "note": note.strip()
                        }

        if not found and search_query:
            st.info(f"❌ Tiada menu ditemui dalam kategori **{category}** yang sepadan dengan '**{search_query}**'.")

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
                st.success(f"🎉 Pesanan untuk **{CustomerName.upper()}** telah dihantar!")
                # Open WhatsApp in new tab
                js = f"""
                <script>
                window.open("{whatsapp_url}", "_blank").focus();
                </script>
                """
                st.markdown(js, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Sila masukkan nama pelanggan.")
    with col2:
        if st.button("🧹 Kosongkan Pesanan"):
            # Reset semua input (qty dan note)
            for category in menu.keys():
                for item in menu[category]:
                    qty_key = f"{category}_{item['name']}_qty"
                    note_key = f"{category}_{item['name']}_note"
                    if qty_key in st.session_state:
                        del st.session_state[qty_key]
                    if note_key in st.session_state:
                        del st.session_state[note_key]
            st.experimental_rerun()
else:
    st.info("🛒 Tiada item dalam pesanan. Sila pilih dari menu di atas.")
