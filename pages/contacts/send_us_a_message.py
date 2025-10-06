# pages/contact_us.py

import streamlit as st

st.title("📩 Contact Us")

st.write(
    """
We'd love to hear from you!  
For questions, collaborations or feedback, reach out directly.
"""
)

# Button to open default mail client
if st.button("Send us an email"):
    st.markdown(
        """
        <a href="mailto:basenghitwitter@gmail.com" target="_blank">
            <button style="background-color:#4CAF50; color:white; padding:10px 20px;
            border:none; border-radius:8px; cursor:pointer; font-size:16px;">
                ✉️ Write to us
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )
