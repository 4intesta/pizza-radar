import streamlit as st

st.write("Manage account")
authenticator = st.session_state.get("authenticator")

# -------------------------
# Logout Button
# -------------------------
if st.button("Logout", type="secondary"):
    authenticator.cookie_controller.delete_cookie()
    st.session_state.clear()
    st.error("Session cleared. The app will now stop.")
    st.stop()