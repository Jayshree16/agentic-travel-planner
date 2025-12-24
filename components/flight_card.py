import streamlit as st

def render_flight_card(flight):
    with st.container(border=True):
        st.markdown("### ✈ Flight Selected")
        st.write(f"**Airline:** {flight['airline']}")
        st.write(f"**Departure:** {flight['departure']}")
        st.write(f"**Arrival:** {flight['arrival']}")
        st.write(f"**Price:** ₹{flight['price']}")
        st.caption(flight.get("reason", ""))
