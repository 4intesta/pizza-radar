import streamlit as st
st.title("Pizza Radar 🍕")

if not st.user.is_logged_in:
    if st.button("Authenticate"):
        st.login("auth0")
else:
    if st.button("Logout"):
        st.logout()