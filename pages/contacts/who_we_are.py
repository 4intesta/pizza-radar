import streamlit as st

# -------------------------
# Preserve Session States
# -------------------------
for k, v in st.session_state.items():
    if k.startswith("card_checkbox"):
        try:
            st.session_state[k] = v
        except st.errors.StreamlitValueAssignmentNotAllowedError:
            pass
        
st.write("Chi siamo")