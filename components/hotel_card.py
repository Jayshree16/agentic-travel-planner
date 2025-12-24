import streamlit as st

def render_hotel_card(hotel):
    with st.container(border=True):
        st.markdown("### 🏨 Hotel Selected")
        st.write(hotel["name"])
        st.write(f"⭐ {hotel['stars']} Stars")
        st.write(f"₹{hotel['price_per_night']} / night")
        st.write(f"Total: ₹{hotel['total_cost']}")
        st.caption(hotel.get("reason", ""))
