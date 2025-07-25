import streamlit as st
import json
import os

# ---------------------- Function: Print to Console ----------------------
def printOrder(CustomerName, TableNum, OrderItem, TotalHarga):
    print("-------------------------------------")
    print(f"{CustomerName.upper()} [Meja Nombor: {TableNum} | Jumlah: RM{TotalHarga:.2f}]")
    print("-------------------------------------")
    for item, details in OrderItem.items():
        subtotal = details["qty"] * details["price"]
        print(f"{item} x {details['qty']} = RM{subtotal:.2f}")
    print("-------------------------------------")

# ---------------------- Function: Save Order to Text File ----------------------
def save_order_to_text(CustomerName, TableNum, OrderItem, TotalHarga, filename="orders.txt"):
    with open(filename, "a") as f:
        f.write("=====================================\n")
        f.write(f"Nama Pelanggan : {CustomerName.upper()}\n")
        f.write(f"Nombor Meja    : {TableNum}\n")
        f.write("-------------------------------------\n")
        for item, details in OrderItem.items():
            qty = details["qty"]
            price = details["price"]
            subtotal = qty * price
            f.write(f"{item} x {qty} = RM{subtotal:.2f}\n")
        f.write("-------------------------------------\n")
        f.write(f"Jumlah         : RM{TotalHarga:.2f}\n")
        f.write("=====================================\n\n")

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
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    st.image(item["img"], width=100)
                with col2:
                    st.subheader(item["name"])
                    st.write(f"💵 Harga: RM{item['price']:.2f}")
                with col3:
                    qty = st.number_input(f"📦 {item['name']}", min_value=0, step=1, key=item['name'])
                    if qty > 0:
                        order_cart[item["name"]] = {"qty": qty, "price": item["price"]}
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
    st.markdown(f"## 💰 Jumlah Keseluruhan: RM{total:.2f}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Hantar Pesanan"):
            if CustomerName.strip():
                printOrder(CustomerName, selected_table, order_cart, total)
                save_order_to_text(CustomerName, selected_table, order_cart, total)
                st.success(f"🎉 Pesanan untuk **{CustomerName.upper()}** telah dihantar dan disimpan dalam fail teks!")
            else:
                st.warning("⚠️ Sila masukkan nama pelanggan.")
    with col2:
        if st.button("🧹 Kosongkan Pesanan"):
            # Padam semua nilai dalam session_state untuk item
            for category in menu.values():
                for item in category:
                    if item["name"] in st.session_state:
                        del st.session_state[item["name"]]
            st.experimental_rerun()
else:
    st.info("🛒 Tiada item dalam pesanan. Sila pilih dari menu di atas.")
import streamlit as st
import json
import os

# ---------------------- Function: Print to Console ----------------------
def printOrder(CustomerName, TableNum, OrderItem, TotalHarga):
    print("-------------------------------------")
    print(f"{CustomerName.upper()} [Meja Nombor: {TableNum} | Jumlah: RM{TotalHarga:.2f}]")
    print("-------------------------------------")
    for item, details in OrderItem.items():
        subtotal = details["qty"] * details["price"]
        print(f"{item} x {details['qty']} = RM{subtotal:.2f}")
    print("-------------------------------------")

# ---------------------- Function: Save Order to Text File ----------------------
def save_order_to_text(CustomerName, TableNum, OrderItem, TotalHarga, filename="orders.txt"):
    with open(filename, "a") as f:
        f.write("=====================================\n")
        f.write(f"Nama Pelanggan : {CustomerName.upper()}\n")
        f.write(f"Nombor Meja    : {TableNum}\n")
        f.write("-------------------------------------\n")
        for item, details in OrderItem.items():
            qty = details["qty"]
            price = details["price"]
            subtotal = qty * price
            f.write(f"{item} x {qty} = RM{subtotal:.2f}\n")
        f.write("-------------------------------------\n")
        f.write(f"Jumlah         : RM{TotalHarga:.2f}\n")
        f.write("=====================================\n\n")

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
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    st.image(item["img"], width=100)
                with col2:
                    st.subheader(item["name"])
                    st.write(f"💵 Harga: RM{item['price']:.2f}")
                with col3:
                    qty = st.number_input(f"📦 {item['name']}", min_value=0, step=1, key=item['name'])
                    if qty > 0:
                        order_cart[item["name"]] = {"qty": qty, "price": item["price"]}
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
    st.markdown(f"## 💰 Jumlah Keseluruhan: RM{total:.2f}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Hantar Pesanan"):
            if CustomerName.strip():
                printOrder(CustomerName, selected_table, order_cart, total)
                save_order_to_text(CustomerName, selected_table, order_cart, total)
                st.success(f"🎉 Pesanan untuk **{CustomerName.upper()}** telah dihantar dan disimpan dalam fail teks!")
            else:
                st.warning("⚠️ Sila masukkan nama pelanggan.")
    with col2:
        if st.button("🧹 Kosongkan Pesanan"):
            # Padam semua nilai dalam session_state untuk item
            for category in menu.values():
                for item in category:
                    if item["name"] in st.session_state:
                        del st.session_state[item["name"]]
            st.experimental_rerun()
else:
    st.info("🛒 Tiada item dalam pesanan. Sila pilih dari menu di atas.")
