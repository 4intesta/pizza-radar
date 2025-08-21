import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import altair as alt
import plotly.express as px
import numpy as np
from numpy.random import default_rng as rng
from random import uniform

import pydeck as pdk

st.set_page_config(layout="wide")

nomePizzeria = "La Mia Pizzeria"
st.title(nomePizzeria)

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


    def generate_competitor_data(n_competitors=20, center_lat=44.783338, center_lon=10.886311):
        """Generate sample competitor data around a center point (Carpi)"""
        competitors = pd.DataFrame({
            'name': [f'Competitor {i+1}' for i in range(n_competitors)],
            'lat': [center_lat + uniform(-0.01, 0.01) for _ in range(n_competitors)],
            'lon': [center_lon + uniform(-0.01, 0.01) for _ in range(n_competitors)],
            'rating': [round(uniform(3.5, 4.8), 1) for _ in range(n_competitors)],
            'interactions': [int(uniform(50, 500)) for _ in range(n_competitors)]
        })
        return competitors

    col4, col5 = st.columns([7, 3], vertical_alignment="bottom")
    with col4:
        with st.container(border=True):
            st.metric("Le Pizze Più Votate Qui Attorno", "", "")

            ##TODO: aggiungere la mia pizzeria alla mappa.

            # Generate competitor data
            competitors_df = generate_competitor_data()

            st.pydeck_chart(
                pdk.Deck(
                    map_style=None,
                    initial_view_state=pdk.ViewState(
                        latitude=44.783338,
                        longitude=10.886311,
                        zoom=13,
                        pitch=0,
                    ),
                    layers=[
                        pdk.Layer(
                            "ScatterplotLayer",
                            data=competitors_df,
                            get_position="[lon, lat]",
                            get_color=[
                                "255 * (1 - (rating - 3.5) / 1.5)",
                                "255 * ((rating - 3.5) / 1.5)",
                                "0",
                                "160"
                            ],
                            # Scale radius based on interactions
                            get_radius="interactions / 2",  # Divide by 2 to get reasonable dot sizes
                            radius_min_pixels=5,           # Minimum size
                            radius_max_pixels=30,          # Maximum size
                            pickable=True,
                            auto_highlight=True,
                        ),
                    ],
                    tooltip={"text": "{name}\nRating: {rating}\nInterazioni: {interactions}"},
                ),
                height= 400
            )

    with col5:
       with st.container(border=True):
          st.markdown("### Riepilogo Recensioni")







            
with tab2:
            
    col1, col2, col3, col4, col5= st.columns([1.35, 1.35, 1.35, 1.35, 1.35], vertical_alignment="bottom")

    with col1:
        st.metric("Prezzo Margherita 🍕", f"{10} €", f"{-0.1} € vs Avg. competitor", border=True)
    
    with col2:
        st.metric("Prezzo Medio 💸", f"{10.5} €", f"{0.1} € vs Avg. competitor", border=True)

    with col3:
        st.metric("Varietà Menu", f"{25}", f"{2} vs Avg. competitor", border=True)

    with col4:
        st.metric("Tempo Massimo di Permanenza ", f"{2} Ore", f"{-10} Minuti vs Avg. competitor", border=True)
    
    with col5:
        st.metric("Tempo Medio di Attesa", f"{25}", f"{-20} Minuti vs Avg. competitor", border=True)

    col6, col7, col8, col9 = st.columns([1.6875, 1.6875, 1.6875, 1.6875], vertical_alignment="bottom")

    with col6:
        with st.container(border=True):
            st.metric("Rating Cibo", f"{4.1}", f"{-0.5} vs Avg. competitor", border=False)
            st.metric("Fra le pizzerie n°", f"{4}", border=False)

    with col7:
        with st.container(border=True):
            st.metric("Rating Servizio", f"{4.1}", f"{-0.5} vs Avg. competitor", border=False)
            st.metric("Fra le pizzerie n°", f"{4}", border=False)

    with col8:
        with st.container(border=True):  
            st.metric("Rating Atmosfera", f"{4.1}", f"{-0.5} vs Avg. competitor", border=False)
            st.metric("Fra le pizzerie n°", f"{4}", border=False)

    with col9:
        with st.container(border=True):
            st.metric("Rating Qualità-Prezzo", f"{4.1}", f"{-0.5} vs Avg. competitor", border=False)
            st.metric("Fra le pizzerie n°", f"{4}", border=False)

    col10, col11,col12 = st.columns([2.25, 2.25, 2.25], vertical_alignment="bottom")

    with col10:
        with st.container(border=True):
            st.metric("Pizzeria Top", "", border=False)
            st.metric("Ultimo Commento", "", border=False)

    with col11:
        with st.container(border=True):
            st.metric("Pizzeria Worst", "", border=False)
            st.metric("Ultimo Commento", "", border=False)

    with col12:
        with st.container(border=True):
            st.metric("Pizzeria in crescita", "", border=False)
            st.metric("Ultimo Commento", "", border=False)