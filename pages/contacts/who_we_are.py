# pages/about_us.py

import streamlit as st

st.title("👥 About Us")

st.write(
    """
We are three management engineers with backgrounds in **strategy, technology, and finance**.  
We built **Lumea** to help restaurants, hotels, bars, and shops transform data and reviews into **concrete actions** that improve results week by week.
"""
)

# Layout: 3 columns for the founders
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Emanuele Casarini")
    st.write("Former **McKinsey** & **Binance**, built AI compliance tools and led due diligence projects.")
    st.caption("Strategy & AI")

with col2:
    st.subheader("Emilio Basenghi")
    st.write("Former **Accenture Strategy**, advised on enterprise IT architecture and delivered agile software projects.")
    st.caption("Technology & Delivery")

with col3:
    st.subheader("Dario Ferrari")
    st.write("Former **Investindustrial**, with private equity experience and published research on cooperative AI systems.")
    st.caption("Finance & Research")

st.markdown("---")

st.write(
    """
Our strength is **complementarity**: we combine strategic consulting, tech delivery, and financial rigor  
to build a product that is simple to use and delivers high operational impact.  
We believe every local business should have access to an **AI copilot** that makes analysis instant and decisions easier.
"""
)
