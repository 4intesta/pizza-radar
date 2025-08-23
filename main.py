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

with st.expander("💡 Analisi AI", expanded=True):
    with st.container(border=True):
        st.badge("Punto di forza", icon="💪", color="green")
    with st.container(border=True):
        st.badge("Punto debole", icon="⚠️", color="orange")
    with st.container(border=True):
        st.badge("Suggerimenti", icon="🛠️", color="blue")

tab1, tab2, tab3 = st.tabs([" 💬 Cosa dicono di noi ", " 🔍 Dentro la nostra Offerta ", " 🍕 Confrontiamoci con pizzerie in zona "])

with tab1:

    df = pd.DataFrame({
                "mese": ["Mag", "Giu", "Lug", "Ago"],
                "positive": [3,6,2,10],
                "negative": [0,-1,-4,-5],
            })

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
    
    # Create sample data for pizza prices
    prices_df = pd.DataFrame({
        'pizzeria': ['La Mia Pizzeria'] + [f'Competitor {i+1}' for i in range(10)],
        'prezzo_margherita': [10.0, 9.5, 11.0, 9.0, 10.5, 8, 11.5, 10.0, 9.0, 10.0, 9.0],
        'prezzo_medio': [12.5, 11.5, 13.0, 11.0, 12.5, 10.5, 13.5, 12.0, 11.0, 12.0, 11.5],
        'menu_items': [45, 38, 42, 35, 40, 32, 48, 41, 37, 43, 39],
        'avg_stay_duration': [2.00, 1.75, 1.92, 1.58, 1.83, 1.50, 2.08, 1.80, 1.67, 1.87, 1.63],  # Hours with 2 decimals
        'wait_time': [5, 15, 5, 6, 6, 6, 4, 5, 6, 5, 5],  # Integer minutes
        'is_mine': [True, False, False, False, False, False, False, False, False, False, False]
    })
    
    # Generate sample monthly ratings for each pizzeria
    np.random.seed(42)  # For reproducible results
    months = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]

    # Define base ratings for all categories
    base_ratings = {
        'cibo': 4.2,
        'servizio': 4.0,
        'atmosfera': 4.1,
        'qualita_prezzo': 3.8
    }

    # Generate ratings for all categories in a single loop
    for category in ['cibo', 'servizio', 'atmosfera', 'qualita_prezzo']:
        for month in months:
            ratings = [
                round(base_ratings[category] + np.random.normal(0, 0.2), 1)
                for _ in range(len(prices_df))
            ]
            # Clip ratings between 3.5 and 5.0
            ratings = np.clip(ratings, 3.5, 5.0)
            prices_df[f'rating_{category}_{month}'] = ratings

    print(prices_df)

    col1, col2, col3 = st.columns([1.35, 1.8, 2.3], vertical_alignment="bottom")

    with col1:
        with st.container(border=True):
            st.metric("Rating", f"{4.5} ⭐️", f"{-0.1} vs competitor")
            st.text("")
            st.metric("Ultimi 30 giorni", f"{4.6} ✨", f"{0.1} su mese precedente")

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
                height=110,
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
                    "size": 100
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
                    alt.Tooltip('Platform:N', title='Piattaforma'),
                    alt.Tooltip('mese_full:N', title='Periodo'),
                    alt.Tooltip('Reviews:Q', title='Recensioni', format='.0f')
                ]
            ).configure_axis(
                labelFontSize=12
            ).configure_legend(
                orient='top',
                title=None
            ).properties(
                height=184,
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
            st.metric("Le Pizze Più Votate Qui Attorno (nell'ultimo mese)", "", "")

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
        def get_articles_data():
            return [
                {
                    "newspaper": "Gazzetta di Modena",
                    "date": "21 Ago 2025",
                    "title": "Le migliori 10 pizzerie di Carpi: la classifica definitiva del 2025",
                    "link": "https://gazzettadimodena.it/news"
                },
                {
                    "newspaper": "Il Resto del Carlino",
                    "date": "19 Ago 2025",
                    "title": "Nuove aperture in centro: le pizzerie che stanno conquistando Carpi",
                    "link": "https://www.ilrestodelcarlino.it/news"
                },
                {
                    "newspaper": "La Repubblica Bologna",
                    "date": "15 Ago 2025",
                    "title": "Pizza gourmet in Emilia: le tendenze del 2025",
                    "link": "https://bologna.repubblica.it/news"
                }
            ]

        with st.container(border=True, height=230):
            articles = get_articles_data()
            st.metric("Ultime Notizie", "", "")
            for article in articles:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <p style="font-size:14px; line-height:1.6;">
                            {article['newspaper']}<br>
                            {article['date']}<br>
                            <a href="{article['link']}" style="text-decoration: none; font-style: italic;">
                                {article['title']}
                            </a>
                        </p>
                        """,
                        unsafe_allow_html=True
                    )

        def get_new_pizzerias_data():
            return [
                {
                    "name": "Pizzeria Nuova",
                    "address": "Via Roma 1, Carpi",
                    "link": "https://www.google.com/maps/place/Via+Roma+1,+Carpi+MO"
                },
                {
                    "name": "Pizzeria Bella Napoli",
                    "address": "Corso Cabassi 10, Carpi",
                    "link": "https://www.google.com/maps/place/Corso+Cabassi+10,+Carpi+MO"
                },
                {
                    "name": "Pizzeria Da Luigi",
                    "address": "Via Cavour 22, Carpi",
                    "link": "https://www.google.com/maps/place/Via+Cavour+22,+Carpi+MO"
                }
            ]

        pizzerias = get_new_pizzerias_data()

        with st.container(border=True, height=230):
            st.metric("Nuove pizzerie in zona", "", "")
            for p in pizzerias:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <p style="font-size:14px; line-height:1.6;">
                            <a href="{p['link']}" style="text-decoration: none; font-weight: bold;">
                                {p['name']}
                            </a><br>
                            <span style="font-style: italic;">{p['address']}</span>
                        </p>
                        """,
                        unsafe_allow_html=True
                    )

with tab2:
    col1, col2 = st.columns([4.1, 1.35], vertical_alignment="bottom")
    with col1:
        with st.container(border=True):
            chart_type = st.selectbox(
                "Seleziona tipologia",
                ["Quanto Costa la Tua Margherita?", "Quanto Costa la tua Pizza in media?"],
                label_visibility="collapsed"
            )
            # Get my values
            my_row = prices_df.loc[prices_df['is_mine']].iloc[0]
            my_margherita_price = my_row['prezzo_margherita']
            my_pizza_media = my_row['prezzo_medio']
            # Get competitor averages
            avg_competitor_margherita = prices_df.loc[~prices_df['is_mine'], 'prezzo_margherita'].mean()
            avg_competitor_pizza = prices_df.loc[~prices_df['is_mine'], 'prezzo_medio'].mean()

            if chart_type == "Quanto Costa la Tua Margherita?":
                st.metric("Prezzo Margherita 🌼", f"{my_margherita_price} €", f"{my_margherita_price - avg_competitor_margherita:.2f} € vs Avg. competitor", delta_color="off", border=False)
                prices_df['prezzo_rounded'] = (prices_df['prezzo_margherita'] * 2).apply(np.floor) / 2
                price_freq = prices_df.groupby('prezzo_rounded').size().reset_index(name='frequency')
                price_freq['prezzo_rounded'] += 0.0001

                my_price = prices_df.loc[prices_df['is_mine'], 'prezzo_rounded'].iloc[0]+ 0.0001

                highlight_value = my_price

                freq_chart = alt.Chart(price_freq).mark_bar(
                    opacity=1
                ).encode(
                    x=alt.X('prezzo_rounded:Q',
                            title=None,
                            bin=alt.Bin(step=0.5),
                            axis=alt.Axis(grid=False)),
                    y=alt.Y('frequency:Q',
                            title=None,
                            axis=alt.Axis(grid=False, labels=False)),
                    color=alt.condition(
                        alt.datum.prezzo_rounded == highlight_value,
                        alt.value("#4285F4"),                             # color if True
                        alt.value("#808080B6")                        # color if False
                    ),
                    tooltip=[
                        alt.Tooltip('prezzo_rounded:Q', title='Prezzo', format='.1f'),
                        alt.Tooltip('frequency:Q', title='Numero Pizzerie')
                    ]
                ).properties(
                    height=188,
                    padding={"left": 5, "top": 0, "right": 5, "bottom": 0}
                )

                final_chart = freq_chart
                st.altair_chart(final_chart, use_container_width=True)
            
            else:  # Pizza media selected
                st.metric("Prezzo Pizza in media 🍕", f"{my_pizza_media} €", f"{my_pizza_media - avg_competitor_pizza:.2f} € vs Avg. competitor", delta_color="off", border=False)
                # Calculate frequency distribution
                prices_df['prezzo_rounded'] = (prices_df['prezzo_medio'] * 2).apply(np.floor) / 2
                avg_price_freq = prices_df.groupby('prezzo_rounded').size().reset_index(name='frequency')
                avg_price_freq['prezzo_rounded'] += 0.0001

                my_avg_price = prices_df.loc[prices_df['is_mine'], 'prezzo_rounded'].iloc[0] + 0.0001

                # Create frequency chart
                avg_freq_chart = alt.Chart(avg_price_freq).mark_bar(
                    opacity=1
                ).encode(
                    x=alt.X('prezzo_rounded:Q',
                            bin=alt.Bin(step=0.5),
                            axis=alt.Axis(grid=False),
                            title=None),
                    y=alt.Y('frequency:Q',
                            axis=alt.Axis(grid=False, labels=False),
                            title=None),
                    color=alt.condition(
                        alt.datum.prezzo_rounded == my_avg_price,
                        alt.value("#4285F4"),      
                        alt.value("#808080B6")    
                    ),
                    tooltip=[
                        alt.Tooltip('prezzo_rounded:Q', title='Prezzo', format='.1f'),
                        alt.Tooltip('frequency:Q', title='Numero Pizzerie')
                    ]
                ).properties(
                    height=188,
                    padding={"left": 5, "top": 0, "right": 5, "bottom": 0}
                )

                # Display the chart
                st.altair_chart(avg_freq_chart, use_container_width=True)
    
    with col2:
        # Get my values and competitor averages
        my_data = prices_df.loc[prices_df['is_mine']].iloc[0]
        avg_competitor_menu = prices_df.loc[~prices_df['is_mine'], 'menu_items'].mean()
        avg_competitor_stay = prices_df.loc[~prices_df['is_mine'], 'avg_stay_duration'].mean()
        avg_competitor_wait = prices_df.loc[~prices_df['is_mine'], 'wait_time'].mean()

        # Update metrics with real data
        st.metric("Nel Menu", 
                    f"{my_data['menu_items']} pizze", 
                    f"{my_data['menu_items'] - avg_competitor_menu:.1f} vs competitor", 
                    border=True)
        
        with st.container(border=True): 
            # Update the metrics to remove the division by 60 since data is already in hours
            st.metric("Permanenza media", 
                        f"{my_data['avg_stay_duration']:.1f} ore", 
                        f"{(my_data['avg_stay_duration'] - avg_competitor_stay):.2f} ore vs competitor", 
                        border=False)
            st.metric("Prima di sedersi", 
                        f"{int(my_data['wait_time'])} min", 
                        f"{int(my_data['wait_time'] - avg_competitor_wait)} min vs competitor", 
                        border=False)
            

    tab_food, tab_service, tab_ambience, tab_quality_price = st.tabs(["🍕 Cibo", "🤵 Servizio ", "🪑 Atmosfera", "💰 Qualità/Prezzo"])


    #TODO: forse ci sarebbe da riformattare gli assi dei 2 grafici in modo che la dimensione degli assi non cambi a seconda della tab

    def render_tab(prices_df, months, month_map, col_prefix, label):
    # Get current month
        current_month = pd.Timestamp.now().strftime("%b")[:3].title()
        month_mapping = {
            "Jan": "Gen", "Feb": "Feb", "Mar": "Mar", "Apr": "Apr",
            "May": "Mag", "Jun": "Giu", "Jul": "Lug", "Aug": "Ago",
            "Sep": "Set", "Oct": "Ott", "Nov": "Nov", "Dec": "Dic"
        }
        current_month = month_mapping[current_month]
        current_month_idx = months.index(current_month)

        # Create ordered list of last 6 months ending with current month
        if current_month_idx >= 5:
            rolling_months = months[current_month_idx - 5: current_month_idx + 1]
        else:
            rolling_months = months[current_month_idx - 5:] + months[:current_month_idx + 1]

        col1, col2 = st.columns([1, 1])

        with col1:
            with st.container(border=True):
                # Get ratings for current category
                my_ratings = prices_df[prices_df['is_mine']][[f"{col_prefix}_{m}" for m in rolling_months]].iloc[0]
                ratings_data = pd.DataFrame({
                    'mese': rolling_months,
                    'rating': my_ratings.values
                })
                ratings_data['mese_full'] = ratings_data['mese'].map(month_map)

                current_rating = my_ratings.values[-1]
                previous_rating = my_ratings.values[-2]
                rating_trend = current_rating - previous_rating
                
                st.metric(f"Rating {label}",
                        f"{current_rating:.1f} ⭐️",
                        f"{rating_trend:+.1f} vs mese precedente",
                        delta_color="normal")

                # Calculate minimum rating across all categories
                categories = ['cibo', 'servizio', 'atmosfera', 'qualita_prezzo']
                all_ratings = []
                for category in categories:
                    category_ratings = prices_df[prices_df['is_mine']][[f"rating_{category}_{m}" for m in rolling_months]].iloc[0]
                    all_ratings.extend(category_ratings.values)
                min_rating = min(all_ratings)

                line_chart = alt.Chart(ratings_data).mark_line(
                    point={"filled": False, "fill": "white", "size": 100}
                ).encode(
                    x=alt.X('mese:O', title=None,
                            axis=alt.Axis(labelAngle=0, grid=False, labelPadding=30),
                            sort=rolling_months),
                    y=alt.Y('rating:Q', title=None,
                            scale=alt.Scale(domain=[min_rating-0.2, 5]),
                            axis=alt.Axis(grid=False)),
                    color=alt.value("#4285F4"),
                    tooltip=[
                        alt.Tooltip('mese_full:N', title='Periodo'),
                        alt.Tooltip('rating:Q', title=f'Rating {label}', format='.1f')
                    ]
                ).properties(height=150, padding={"left": 5, "top": 5, "right": 0, "bottom": 5})
                
                st.altair_chart(line_chart, use_container_width=True)

        with col2:
            with st.container(border=True):
                my_rating = prices_df.loc[prices_df['is_mine'], f"{col_prefix}_Dic"].iloc[0]
                competitor_ratings = prices_df.loc[~prices_df['is_mine'], f"{col_prefix}_Dic"]
                avg_competitor_rating = competitor_ratings.mean()
                
                st.metric(f"Rating {label}",
                        f"{my_rating:.1f} ⭐️",
                        f"{(my_rating - avg_competitor_rating):.2f} vs Avg. competitor",
                        delta_color="normal")

                # Update rating rounding to 0.2 steps
                prices_df['rating_rounded'] = (prices_df[f"{col_prefix}_Dic"] * 5).apply(np.floor) / 5
                rating_freq = prices_df.groupby('rating_rounded').size().reset_index(name='frequency')
                rating_freq['rating_rounded'] += 0.0001
                my_rating_rounded = prices_df.loc[prices_df['is_mine'], 'rating_rounded'].iloc[0] + 0.0001

                # Get minimum rating for dynamic scale
                min_rating_bin = rating_freq['rating_rounded'].min()

                freq_chart = alt.Chart(rating_freq).mark_bar(opacity=1).encode(
                    x=alt.X('rating_rounded:Q', 
                            title=None,
                            bin=alt.Bin(step=0.2),
                            scale=alt.Scale(domain=[min_rating_bin, 5.0001]),
                            axis=alt.Axis(
                                grid=False,
                                values=list(np.arange(min_rating_bin, 5.1, 0.2))
                            )),
                    y=alt.Y('frequency:Q', 
                            title=None,
                            axis=alt.Axis(grid=False, labels=False)),
                    color=alt.condition(
                        alt.datum.rating_rounded == my_rating_rounded,
                        alt.value("#4285F4"), 
                        alt.value("#808080B6")),
                    tooltip=[
                        alt.Tooltip('rating_rounded:Q', title='Rating', format='.1f'),
                        alt.Tooltip('frequency:Q', title='Numero Pizzerie')
                    ]
                ).properties(
                    height=150, 
                    padding={"left": 5, "top": 0, "right": 5, "bottom": 0}
                )

                st.altair_chart(freq_chart, use_container_width=True)

    with tab_food:
        render_tab(prices_df, months, month_map, "rating_cibo", "Cibo")

    with tab_service:
        render_tab(prices_df, months, month_map, "rating_servizio", "Servizio")

    with tab_ambience:
        render_tab(prices_df, months, month_map, "rating_atmosfera", "Atmosfera")

    with tab_quality_price:
        render_tab(prices_df, months, month_map, "rating_qualita_prezzo", "Qualità/Prezzo")

with tab3:
    # Store selectbox value in a variable
    selected_pizzeria = st.selectbox(
        "Confronta la tua pizzera con altre in zona", 
        options=prices_df[prices_df['is_mine'] == False]['pizzeria'].tolist(), 
        index=None,
        placeholder="Scegli una pizzeria in zona...", 
        label_visibility="collapsed"
    )
    
    def create_comparison_chart(prices_df, selected_pizzeria, months, category):
        """Helper function to create comparison charts with rolling 12 months"""
        # Get current month
        current_month = pd.Timestamp.now().strftime("%b")[:3].title()  # Get first 3 letters of month name
        # Map Italian months
        month_mapping = {
            "Jan": "Gen", "Feb": "Feb", "Mar": "Mar", "Apr": "Apr",
            "May": "Mag", "Jun": "Giu", "Jul": "Lug", "Aug": "Ago",
            "Sep": "Set", "Oct": "Ott", "Nov": "Nov", "Dec": "Dic"
        }
        current_month = month_mapping[current_month]
        current_month_idx = months.index(current_month)
        
        # Create ordered list of last 12 months ending with current month
        rolling_months = months[current_month_idx - 11:] + months[:current_month_idx + 1]
        
        # Calculate minimum rating across ALL categories and ALL months
        categories = ['cibo', 'servizio', 'atmosfera', 'qualita_prezzo']
        all_ratings = []
        
        for cat in categories:
            # Get ratings from my pizzeria
            my_ratings = prices_df[prices_df['is_mine']][[f'rating_{cat}_{m}' for m in rolling_months]].iloc[0]
            # Get ratings from selected competitor
            competitor_ratings = prices_df[prices_df['pizzeria'] == selected_pizzeria][[f'rating_{cat}_{m}' for m in rolling_months]].iloc[0]
            all_ratings.extend(my_ratings.values)
            all_ratings.extend(competitor_ratings.values)
        
        global_min_rating = min(all_ratings)
        
        # Get ratings for current category
        my_ratings = prices_df[prices_df['is_mine']][[f'rating_{category}_{m}' for m in rolling_months]].iloc[0]
        competitor_ratings = prices_df[prices_df['pizzeria'] == selected_pizzeria][[f'rating_{category}_{m}' for m in rolling_months]].iloc[0]
        
        comparison_df = pd.DataFrame({
            'mese': rolling_months,
            'La Mia Pizzeria': my_ratings.values,
            'Competitor': competitor_ratings.values
        })
        
        comparison_melted = comparison_df.melt(
            id_vars=['mese'],
            var_name='Pizzeria',
            value_name='Rating'
        )
        
        # Update y-axis scale to use global minimum
        return alt.Chart(comparison_melted).mark_line(
            point={"filled": False, "fill": "white", "size": 100}
        ).encode(
            x=alt.X('mese:O',
                   title=None,
                   axis=alt.Axis(
                       labelAngle=0,
                       grid=False
                   ),
                   sort=rolling_months),
            y=alt.Y('Rating:Q',
                   scale=alt.Scale(domain=[global_min_rating-0.2, 5]),
                   title=None,
                   axis=alt.Axis(grid=True)),
            color=alt.Color('Pizzeria:N',
                          scale=alt.Scale(
                              domain=['La Mia Pizzeria', 'Competitor'],
                              range=['#F12929', '#4285F4']
                          )),
            tooltip=[
                alt.Tooltip('Pizzeria:N', title='Pizzeria'),
                alt.Tooltip('mese:N', title='Periodo'),
                alt.Tooltip('Rating:Q', title='⭐ Rating', format='.1f')
            ]
        ).properties(
            height=227,
            padding={"left": 5, "top": 0, "right": 5, "bottom": 5}
        ).configure_axis(
            labelFontSize=12
        ).configure_legend(
            orient='top',
            title=None
        )
    
    # Only show tabs if a pizzeria is selected
    if selected_pizzeria:
        tab_comparison_cibo, tab_comparison_servizio, tab_comparison_atmosfera, tab_comparison_qualita_prezzo = st.tabs([
            "🍕 Cibo", 
            "🤵 Servizio ", 
            "🪑 Atmosfera", 
            "💰 Qualità/Prezzo"
        ])
        
        def render_comparison_tab(prices_df, selected_pizzeria, months, category, label):
            """Helper function to render comparison tab layout"""
            col1, col2 = st.columns([1.35, 4.1])
    
            with col1:    
                with st.container(border=True):
                    st.metric(f"Rating {label}", f"{4.5} ⭐️", f"{-0.1} vs competitor")
                    st.text("")
                    st.metric("Ultimi 30 giorni", f"{4.6} ✨", f"{0.1} su mese precedente")
    
            with col2:
                with st.container(border=True):
                    chart = create_comparison_chart(prices_df, selected_pizzeria, months, category)
                    st.altair_chart(chart, use_container_width=True)

        with tab_comparison_cibo:
            render_comparison_tab(prices_df, selected_pizzeria, months, 'cibo', 'Cibo')
            
        with tab_comparison_servizio:
            render_comparison_tab(prices_df, selected_pizzeria, months, 'servizio', 'Servizio')
            
        with tab_comparison_atmosfera:
            render_comparison_tab(prices_df, selected_pizzeria, months, 'atmosfera', 'Atmosfera')
            
        with tab_comparison_qualita_prezzo:
            render_comparison_tab(prices_df, selected_pizzeria, months, 'qualita_prezzo', 'Qualità/Prezzo')
