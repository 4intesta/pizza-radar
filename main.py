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

tab1, tab2, tab3 = st.tabs([" 💬 Cosa dicono di noi ", " 🔍 Dentro la nostra Offerta ", " 🍕 Testa a Testa "])

with tab1:

    df = pd.DataFrame({
                "mese": ["Set", "Ott", "Nov", "Dic"],
                "positive": [3,6,2,10],
                "negative": [0,-1,-4,-5],
            })
    print(df)

    month_map = {
        "Gen": "Gennaio",
        "Feb": "Febbraio",
        "Mar": "Marzo",
        "Apr": "Aprile",
        "Mag": "Maggio",
        "Giu": "Giugno",
        "Lug": "Luglio",
        "Ago": "Agosto",
        "Set": "Settembre",
        "Ott": "Ottobre",
        "Nov": "Novembre",
        "Dic": "Dicembre"
    }
    
    col1, col2, col3 = st.columns([1.35, 1.8, 2.3], vertical_alignment="bottom")


    # Create container for metrics in col1
    with col1:
        st.metric("Rating", f"{4.5} ⭐️", f"{-0.1} vs competitor", border=True)
        st.metric("Trend Rating", f"{4.6} ✨", f"{0.1} su {df['mese'].iloc[-2]}", border=True)

    with col2:
        with st.container(border=True):
            
            df["mese_full"] = df["mese"].map(month_map)

            labelValueRecensioniMensili = df['positive'].iloc[-1]-df['negative'].iloc[-1]
            valueRecensioniMensiliScorsoMese = df['positive'].iloc[-2]-df['negative'].iloc[-2]
            monthlyDifference =  (labelValueRecensioniMensili/valueRecensioniMensiliScorsoMese)*100
            st.metric("Recensioni Mese Corrente", f"{labelValueRecensioniMensili}", f"{monthlyDifference}% su {df['mese'].iloc[-2]}")

            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('mese:O', 
                        title=None,
                        axis=alt.Axis(
                            grid=False, 
                            labelAngle=0,
                            labelPadding=0,
                        ),
                        sort=["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]),
                y=alt.Y('value:Q', 
                        title=None,
                        axis=alt.Axis(grid=False, labels=False)),
                color=alt.Color('variable:N', 
                  scale=alt.Scale(range=['#F12929', '#62d41c']), 
                  legend=None),
                tooltip=[
                    alt.Tooltip('mese_full:N', title='Periodo'),
                    alt.Tooltip('tipo:N', title='Valutazione'),
                    alt.Tooltip('abs_value:Q', title='Recensioni', format='.0f')
                ]
            ).transform_fold(
                ['positive', 'negative'],
                as_=['variable', 'value']
            ).transform_calculate(
                abs_value="abs(datum.value)",
                tipo="datum.variable == 'positive' ? 'Positiva' : 'Negativa'"  # Add mapping here
            ).properties(
                height=127,
                padding={"left": 0, "top": 0, "right": 0, "bottom": 0}
            )
            st.altair_chart(chart, use_container_width=True)

    with col3:
        with st.container(border=True):
            
            # Replace markdown with metric
            st.metric("Recensioni per Piattaforma", "", "")
            
            # Create sample data for reviews by platform
            line_data = pd.DataFrame({
                'mese': ["Set", "Ott", "Nov", "Dic"],
                'Google': [15, 18, 20, 25],
                'Deliveroo': [8, 12, 10, 15],
                'TripAdvisor': [5, 7, 6, 10]
            })

            # Add total reviews column
            line_data['Totale'] = line_data[['Google', 'Deliveroo', 'TripAdvisor']].sum(axis=1)

            # Melt the dataframe for Altair
            line_data_melted = line_data.melt(
                id_vars=['mese'], 
                value_vars=['Totale', 'Google', 'Deliveroo', 'TripAdvisor'],  # Add Totale to value_vars
                var_name='Platform',
                value_name='Reviews'
            )
            line_data_melted["mese_full"] = line_data_melted["mese"].map(month_map)

            max_reviews = np.ceil(line_data_melted['Reviews'].max())

            # Create Altair line chart
            line_chart = alt.Chart(line_data_melted).mark_line(
                point={
                    "filled": False,
                    "fill": "white",
                    "size": 60
                }
            ).encode(
                x=alt.X('mese:O', 
                       title=None,
                       axis=alt.Axis(
                           labelAngle=0,
                           grid=False,
                           labelPadding=10
                       ),
                       sort=["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]),
                y=alt.Y('Reviews:Q',
                       title=None,
                       scale=alt.Scale(domain=[0, max_reviews]),
                       axis=alt.Axis(
                           grid=False,
                           labels=False
                       )),
                color=alt.Color('Platform:N',
                              scale=alt.Scale(
                                  domain=['Totale', 'Google', 'Deliveroo', 'TripAdvisor'],
                                  range=["#808080B6", '#4285F4', '#5cc9bc', '#6be76e']
                              ),
                              legend=alt.Legend(
                                  values=['Google', 'Deliveroo', 'TripAdvisor']  # Only show these in legend
                              )),
                tooltip=[
                    alt.Tooltip('mese_full:N', title='Periodo'),
                    alt.Tooltip('Platform:N', title='Piattaforma'),
                    alt.Tooltip('Reviews:Q', title='Recensioni', format='.0f')
                ]
            ).configure_axis(
                labelFontSize=12
            ).configure_legend(
                orient='top',
                title=None
            ).properties(
                height=200,
                padding={"left": -5, "top": -5, "right": 0, "bottom": 0}
            )

            # Render the chart
            st.altair_chart(line_chart, use_container_width=True)
