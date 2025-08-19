import config  # Must be the very first import
import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import plotly.express as px
import numpy as np

st.title("La Mia Pizzeria")

# Create tabs
tab1, tab2 = st.tabs(["📊 La mia performance", "📈 Analisi Competitiva"])
