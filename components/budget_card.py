import streamlit as st

def render_budget(budget):
    with st.container(border=True):
        st.markdown("### 💰 Budget Breakdown")
        st.write("Flight:", budget["flight"])
        st.write("Hotel:", budget["hotel"])
        st.write("Local:", budget["local_expenses"])
        st.success(f"Total Cost: ₹{budget['total']}")
