import streamlit as st
# -------------------------
# Preserve Session States
# -------------------------

st.write("Manage account")

if st.session_state.get("authentication_status"):
    authenticator = st.session_state.get("authenticator")
    authenticator.logout(location="main", key="logout-demo-app-page-1")


elif st.session_state == {} or st.session_state["authentication_status"] is None:
    st.warning("Please use the button below to navigate to Home and log in.")
    st.page_link("Home.py", label="Home", icon="🏠 ")
    st.stop()