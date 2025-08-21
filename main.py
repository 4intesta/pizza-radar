import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import altair as alt
import plotly.express as px
import numpy as np
from numpy.random import default_rng as rng


st.set_page_config(layout="wide")


st.title("La Mia Pizzeria")

st.expander("💡 Analisi AI", expanded=True)

with st.container(border=True): #l'ho messo perchè se no sfarfalla quando espando/contraggo Analisi AI
    tab1, tab2, tab3 = st.tabs([" 💬 Cosa dicono di noi ", " 🔍 Dentro la nostra Offerta ", " 🍕 Testa a Testa "])

    with tab1:
        col1, col2, col3 = st.columns([1, 1.5, 2.5], vertical_alignment="bottom")

        # Create container for metrics in col1
        with col1:
            st.metric("Rating", f"{4.5} ⭐️", f"{-0.1} rispetto media competitor", border=True)
            st.metric("New Metric", "Value", "Delta", border=True)

        with col2:
            with st.container(border=True):
                st.metric("Trend Recensioni", f"{4.5} questo mese", "-9°F")

                df = pd.DataFrame({
                    "period": ["maggio", "giugno", "luglio", "agosto"],
                    "positive": [3,6,2,10],   # Around 10, some variation
                    "negative": [0,-1,-4,-5], # Around -10, some variation
                })
                print(df)

                # Create a custom sort order for months
                month_order = df['period'].tolist()

                chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X('period:O', 
                            title=None,
                            axis=alt.Axis(grid=False),
                            sort=month_order),
                    y=alt.Y('value:Q', 
                            title=None,
                            axis=alt.Axis(grid=False, labels=False)),
                    color=alt.Color('variable:N', 
                                scale=alt.Scale(range=['#F12929', '#62d41c']), 
                                legend=None),
                ).transform_fold(
                    ['positive', 'negative'],
                    as_=['variable', 'value']
                )

                st.altair_chart(chart, use_container_width=True)

        with col3:
            with st.container(border=True):
                # Create sample data for multiple lines
                line_data = pd.DataFrame({
                    'date': pd.date_range(start='2024-01-01', periods=12, freq='M'),
                    'Rating Generale': [4.2, 4.3, 4.1, 4.4, 4.2, 4.5, 4.3, 4.2, 4.4, 4.5, 4.3, 4.4],
                    'Rating Cibo': [4.3, 4.4, 4.2, 4.5, 4.3, 4.6, 4.4, 4.3, 4.5, 4.6, 4.4, 4.5],
                    'Rating Servizio': [4.1, 4.2, 4.0, 4.3, 4.1, 4.4, 4.2, 4.1, 4.3, 4.4, 4.2, 4.3],
                    'Rating Ambiente': [4.2, 4.3, 4.1, 4.4, 4.2, 4.5, 4.3, 4.2, 4.4, 4.5, 4.3, 4.4]
                })

                # Create line chart options with multiple series
                line_options = {
                    "tooltip": {
                        "trigger": "axis",
                        "formatter": "{b}<br/>{a}: {c}"
                    },
                    "legend": {
                        "data": ["Rating Generale", "Rating Cibo", "Rating Servizio", "Rating Ambiente"],
                        "orient": "horizontal",
                        "top": "top",
                        "textStyle": {"fontSize": 12}
                    },
                    "grid": {
                        "left": "3%",
                        "right": "4%",
                        "bottom": "15%",
                        "top": "15%",
                        "containLabel": True
                    },
                    "xAxis": {
                        "type": "category",
                        "data": [d.strftime('%m/%Y') for d in line_data['date']],
                        "axisLabel": {
                            "fontSize": 12,
                            "rotate": 45
                        }
                    },
                    "yAxis": {
                        "type": "value",
                        "min": 3.5,
                        "max": 5,
                        "interval": 0.5,
                        "axisLabel": {"fontSize": 12}
                    },
                    "series": [
                        {
                            "name": "Rating Generale",
                            "data": line_data['Rating Generale'].tolist(),
                            "type": "line",
                            "smooth": True,
                            "lineStyle": {"width": 2},
                            "symbol": "circle",
                            "symbolSize": 6,
                            "itemStyle": {"color": "#5470c6"}
                        },
                        {
                            "name": "Rating Cibo",
                            "data": line_data['Rating Cibo'].tolist(),
                            "type": "line",
                            "smooth": True,
                            "lineStyle": {"width": 2},
                            "symbol": "circle",
                            "symbolSize": 6,
                            "itemStyle": {"color": "#91cc75"}
                        },
                        {
                            "name": "Rating Servizio",
                            "data": line_data['Rating Servizio'].tolist(),
                            "type": "line",
                            "smooth": True,
                            "lineStyle": {"width": 2},
                            "symbol": "circle",
                            "symbolSize": 6,
                            "itemStyle": {"color": "#fac858"}
                        },
                        {
                            "name": "Rating Ambiente",
                            "data": line_data['Rating Ambiente'].tolist(),
                            "type": "line",
                            "smooth": True,
                            "lineStyle": {"width": 2},
                            "symbol": "circle",
                            "symbolSize": 6,
                            "itemStyle": {"color": "#ee6666"}
                        }
                    ]
                }
                
                # Render the chart
                st_echarts(options=line_options)
