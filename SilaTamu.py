import streamlit as st
import json


def printOrder(TableNum,OrderItem,TotalHarga):
    print("--------------------------------")
    print("Meja Nombor : " + str(TableNum) + f" (RM {TotalHarga:.2f})")
    print("--------------------------------")
    for item,details in OrderItem.items():
        print(f"{item} x {details['qty']} = RM{subtotal:.2f}")

# Sample menu data
with open('SilaTamu-Menu.json') as myMenu:
    menu = json.load(myMenu)

# App title
st.title("🍽️ SilaTamu 🍽️")
selected_table = st.selectbox("Pilih nombor meja:", list(range(1, 11)))
st.write(f"🪑 Meja nombor: {selected_table}")
# Create tabs for each category
tabs = st.tabs(list(menu.keys()))

# Dictionary to hold orders
order_cart = {}

# Loop through each tab/category
for i, category in enumerate(menu.keys()):
    with tabs[i]:
        st.header(category)
        for item in menu[category]:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(item["img"], width=120)
            with col2:
                st.subheader(item["name"])
                st.write(f"Price: RM{item['price']:.2f}")
                qty = st.number_input(f"Quantity - {item['name']}", min_value=0, step=1, key=item['name'])
                if qty > 0:
                    order_cart[item["name"]] = {"qty": qty, "price": item["price"]}

# Show Order Summary
st.markdown("---")
st.subheader("🧾 Order Summary")

if order_cart:
    total = 0
    for item, details in order_cart.items():
        subtotal = details["qty"] * details["price"]
        total += subtotal
        st.write(f"{item} x {details['qty']} = RM{subtotal:.2f}")
    st.markdown(f"### Total: RM{total:.2f}")
    if st.button("✅ Place Order"):
        printOrder(selected_table,order_cart,total)
        st.write(f"🪑 Meja nombor: {selected_table}")
        for item, details in order_cart.items():
            subtotal = details["qty"] * details["price"]
            total += subtotal
            st.write(f"{item} x {details['qty']} = RM{subtotal:.2f}")
        
else:
    st.info("No items selected yet.")
