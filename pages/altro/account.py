import streamlit as st
st.title("Il tuo account")

st.write(f'**Nome Account:** {st.user["nickname"]}')
st.write(f"**Email:** {st.user['email']}")
if st.user['email_verified'] is True:
    st.write(f"**Email Verificata:** :material/check:")
if st.user['email_verified'] is False:
    st.write(f"**Email Verificata:** :material/close:")


if st.button("Logout"):
    st.logout()