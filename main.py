import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")
st.title("La Mia Pizzeria")

st.expander("💡 Analisi AI", expanded=True)

tab1, tab2, tab3 = st.tabs([" 💬 Cosa dicono di noi ", " 🔍 Dentro la nostra Offerta ", " 🍕 Testa a Testa "])

