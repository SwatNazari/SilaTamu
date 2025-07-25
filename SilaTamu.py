import streamlit as st
import json

# Sample menu data
with open('SilaTamu-Menu.json') as myMenu:
    menu = json.load(myMenu)

# App title
st.title("🍽️ SilaTamu 🍽️")

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
        print("Sent Order")
else:
    st.info("No items selected yet.")
