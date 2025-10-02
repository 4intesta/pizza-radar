import streamlit as st
# -------------------------
# Preserve Session States
# -------------------------
for k, v in st.session_state.items():
    st.session_state[k] = v

st.write("Manage account")
if st.button("Log out"):
    pg = st.navigation({"": [st.Page("pages/dashboard/kpis_general.py")]}, position="hidden")
    pg.run()
    st.session_state["user_logged"] = False
    st.rerun()
