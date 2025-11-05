import streamlit as st
import pandas as pd
import numpy as np
from numpy.random import default_rng as rng
from random import uniform
import pydeck as pdk

# Add these DataFrames before tab1
best_pizzeria = pd.DataFrame({
    'name': ['Pizzeria Da Michele'],
    'rating': [4.8],
    'rating_trend_su_mese': ['0.1'],
    'total_reviews': [856],
    'total_reviews_trend_su_mese': ['30'],
    'specialty': ['Pizza Napoletana'],
    'top_comments': [[
        {
            'author': 'Marco R.',
            'date': '20 Ago 2025',
            'rating': 5,
            'text': 'La migliore pizza napoletana in zona. Impasto perfetto.'
        },
        {
            'author': 'Laura B.',
            'date': '18 Ago 2025',
            'rating': 5,
            'text': 'Vale ogni centesimo. La marinara è sublime!'
        },
        {
            'author': 'Giovanni M.',
            'date': '15 Ago 2025',
            'rating': 5,
            'text': 'Finalmente una vera pizza napoletana.'
        }
    ]]
})

worst_pizzeria = pd.DataFrame({
    'name': ['Pizzeria Lo Scoglio'],
    'rating': [2.8],
    'total_reviews': [234],
    'specialty': ['Pizza'],
    'rating_trend_su_mese': ['-0.3'],
    'total_reviews_trend_su_mese': ['-5'],
    'top_comments': [[
        {
            'author': 'Paolo M.',
            'date': '19 Ago 2025',
            'rating': 1,
            'text': 'Tempi di attesa lunghissimi e pizza fredda.'
        },
        {
            'author': 'Sara T.',
            'date': '17 Ago 2025',
            'rating': 2,
            'text': 'Servizio scadente e prezzi troppo alti.'
        },
        {
            'author': 'Luigi B.',
            'date': '16 Ago 2025',
            'rating': 2,
            'text': 'Qualità in netto peggioramento.'
        }
    ]]
})

trending_pizzeria = pd.DataFrame({
    'name': ['Pizzeria Bella Napoli'],
    'rating': [4.2],
    'total_reviews': [345],
    'specialty': ['Pizza Contemporanea'],
    'rating_trend_su_mese': ['0.8'],
    'total_reviews_trend_su_mese': ['10'],
    'top_comments': [[
        {
            'author': 'Elena F.',
            'date': '21 Ago 2025',
            'rating': 5,
            'text': 'Che miglioramento! Nuova gestione fantastica.'
        },
        {
            'author': 'Roberto D.',
            'date': '19 Ago 2025',
            'rating': 4,
            'text': 'Grande svolta, ora è tra le migliori.'
        },
        {
            'author': 'Maria C.',
            'date': '17 Ago 2025',
            'rating': 4,
            'text': 'Finalmente un servizio eccellente.'
        }
    ]]
})

def render_review_tab(pizzeria_data, tab_type):
        """Helper function to render review tabs (migliore, peggiore, di moda)"""
        st.subheader(f"*{pizzeria_data['name'].iloc[0]}*")
        col1, col2 = st.columns([1.35, 4.1])
        
        with col1:
            st.metric(
                "**Rating Generale**", 
                f"{pizzeria_data['rating'].iloc[0]} ⭐️", 
                f"{pizzeria_data['rating_trend_su_mese'].iloc[0]} su mese", 
                border=True
            )
            
            changes = list(rng(4).standard_normal(20))
            st.metric(
                "**Recensioni Ricevute**", 
                pizzeria_data['total_reviews'].iloc[0], 
                f"{pizzeria_data['total_reviews_trend_su_mese'].iloc[0]}  su mese",
                chart_data=[sum(changes[:i]) for i in range(20)], 
                chart_type="line",
                border=True
            )
        
        with col2:
            st.write("Recensioni recenti:")
            with st.container(height=322, border=False):
                for comment in pizzeria_data['top_comments'].iloc[0]:
                    with st.container(border=False):
                        source = "Google" if comment['rating'] > 3 else "TripAdvisor"  # Example logic
                        if(tab_type!="PEGGIOORE"):
                            st.success(
                                f":small[***{comment['author']} ({comment['date']})***  \n {source}]  \n"
                                f":small[*{comment['text']}*]  ↗"
                            )
                        else:
                            st.error(
                                f":small[***{comment['author']} ({comment['date']})***  \n {source}]  \n"
                                f":small[*{comment['text']}*]  ↗"
                            )


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

prices_df = pd.DataFrame({
    'pizzeria': ['La Mia Pizzeria'] + [f'Competitor {i+1}' for i in range(10)],
    'prezzo_margherita': [10.0, 9.5, 11.0, 9.0, 10.5, 8, 11.5, 10.0, 9.0, 10.0, 9.0],
    'prezzo_medio': [12.5, 11.5, 13.0, 11.0, 12.5, 10.5, 13.5, 12.0, 11.0, 12.0, 11.5],
    'menu_items': [45, 38, 42, 35, 40, 32, 48, 41, 37, 43, 39],
    'avg_stay_duration': [2.00, 1.75, 1.92, 1.58, 1.83, 1.50, 2.08, 1.80, 1.67, 1.87, 1.63],
    'historic_generale_rating': [4.3, 3.9, 4.1, 3.7, 4.0, 3.8, 4.2, 4.0, 3.8, 4.1, 3.9],
    'average_rating_generale_last_7_days': [4.5, 4.0, 4.2, 3.8, 4.1, 3.9, 4.3, 4.1, 3.9, 4.2, 4.0],
    'average_rating_generale_last_7_14_days': [4.5, 4.0, 4.2, 3.8, 4.1, 3.9, 4.3, 4.1, 3.9, 4.2, 4.0],
    'average_rating_generale_last_30_days': [4.6, 4.2, 4.3, 4.1, 4.4, 4.0, 4.5, 4.2, 4.1, 4.3, 4.2],
    'reviews_number_last_7_days': [12, 10, 11, 9, 13, 8, 14, 10, 9, 11, 10],
    'reviews_number_last_7_14_days': [15, 12, 14, 11, 13, 10, 16, 12, 11, 14, 12],
    'reviews_number_last_30_days': [42, 35, 38, 31, 36, 28, 40, 33, 30, 37, 32],
    'weekly_reviews': [
        [0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5, 6]
    ],
    'day_average_rating': [
        [1, None, None, 5, 5, 5, 5],
        [None, 3, 3.5, 3, 4, 5, None],
        [1, 1, 2, 3, 4, 5, 4.5],
        [1, 1, 2, 3, 4, 5, 4.5],
        [1, 1, 2, 3, 4, 5, 4.5],
        [1, 1, 2, 3, 4, 5, 4.5],
        [1, 1, 2, 3, 4, 5, 4.5],
        [1, 1, 2, 3, 4, 5, 4.5],
        [1, 1, 2, 3, 4, 5, 4.5],
        [1, 1, 2, 3, 4, 5, 4.5],
        [1, 1, 2, 3, 4, 5, 4.5]
    ],
    'is_mine': [True, False, False, False, False, False, False, False, False, False, False]
})

# ➕ Add "distance_from_you" attribute (in km)
# The first one (La Mia Pizzeria) is 0 km; others random between 0.2 and 5 km
np.random.seed(42)  # for reproducibility
distances = [0] + list(np.round(np.random.uniform(0.2, 5.0, 10), 2))
prices_df['distance_from_you'] = distances


# Compute the new fields
prices_df['competio_valutazione_current'] = (
    prices_df['reviews_number_last_7_days'] *
    (prices_df['average_rating_generale_last_7_days'] - 3)
)

prices_df['competio_valutazione_last_week'] = (
    prices_df['average_rating_generale_last_7_14_days'] *
    (prices_df['average_rating_generale_last_7_14_days'] - 3)
)

# Compute rankings (1 = best performer)
prices_df['competio_ranking_current'] = (
    prices_df['competio_valutazione_current']
    .rank(ascending=False, method='min')
    .astype(int)
)

prices_df['competio_ranking_last_week'] = (
    prices_df['competio_valutazione_last_week']
    .rank(ascending=False, method='min')
    .astype(int)
)

# Display a preview of the rankings
print(prices_df[['pizzeria', 'competio_valutazione_current', 'competio_ranking_current',
                 'competio_valutazione_last_week', 'competio_ranking_last_week']])


# Generate sample monthly ratings for each pizzeria
np.random.seed(42)  # For reproducible results
months = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]

# Define base ratings for all categories
base_ratings = {
    'generale': 3.0,
    'cibo': 4.2,
    'servizio': 4.0,
    'atmosfera': 4.1,
    'qualita_prezzo': 3.8
}

# Generate ratings for all categories in a single loop
for category in ['generale', 'cibo', 'servizio', 'atmosfera', 'qualita_prezzo']:
    for month in months:
        ratings = [
            round(base_ratings[category] + np.random.normal(0, 0.2), 1)
            for _ in range(len(prices_df))
        ]
        # Clip ratings between 3.5 and 5.0
        ratings = np.clip(ratings, 1, 5.0)
        prices_df[f'rating_{category}_{month}'] = ratings

print(prices_df)

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

st.subheader("Panoramica Concorrenza")
st.write("Nella tua zona ci sono diverse pizzerie. Ecco una panoramica delle loro performance e di come si posiziona la tua:")

with st.container(border=False):
    
    # Generate competitor data
    competitors_df = generate_competitor_data()

    # Add my pizzeria data to competitors_df
    my_pizzeria_data = pd.DataFrame({
        'name': ['La Mia Pizzeria'],
        'lat': [44.784338],  # Slightly offset from center
        'lon': [10.887311],  # Slightly offset from center
        'rating': [prices_df.loc[prices_df['is_mine'], 'historic_generale_rating'].iloc[0]],
        'interactions': [450]  # High number of interactions for visibility
    })

    # Combine my pizzeria with competitors
    all_pizzerias = pd.concat([my_pizzeria_data, competitors_df])

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
                # Layer for competitor pizzerias
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
                # Additional layer for my pizzeria with border
                pdk.Layer(
                    "ScatterplotLayer",
                    data=my_pizzeria_data,
                    get_position="[lon, lat]",
                    get_color=[
                        "255 * (1 - (rating - 3.5) / 1.5)",
                        "255 * ((rating - 3.5) / 1.5)",
                        "0",
                        "160"
                    ],
                    get_radius="interactions / 2",
                    radius_min_pixels=5,
                    radius_max_pixels=30,
                    pickable=True,
                    auto_highlight=True,
                    stroked=True,  # enable borders
                    line_width_min_pixels=1.5,  # border width
                    get_line_color=[0, 0, 0]  # border color (gray here)
                ),
            ],
            tooltip={"text": "{name}\nRating: {rating}\nInterazioni: {interactions}"},
        ),
        height=400
    )

# Configure the dataframe display
# Sort by ascending rank (1 = best)
sorted_df = prices_df.sort_values(by="competio_ranking_current", ascending=True)

st.dataframe(
    sorted_df[[
        "competio_ranking_current",
        "pizzeria",
        "average_rating_generale_last_7_days",
        "reviews_number_last_7_days",
        "weekly_reviews",
        "prezzo_medio",
        "distance_from_you"
    ]],
    column_config={
        "competio_ranking_current": st.column_config.NumberColumn(
            "Classifica",
            width=4,
            help="Valutazione attuale su Compet.io"
        ),
        "pizzeria": st.column_config.TextColumn(
            "Pizzeria",
            width=150,
            help="Nome della pizzeria"
        ),
        "average_rating_generale_last_7_days": st.column_config.ProgressColumn(
            "Generale ⭐️",
            format="%.1f",
            width=100,
            min_value=0,
            max_value=5,
            help="Valutazione generale ultimi 7 giorni"
        ),
        "reviews_number_last_7_days": st.column_config.NumberColumn(
            "Numero Recensioni",
            width=100,
            help="Numero di recensioni negli ultimi 7 giorni"
        ),
        "prezzo_medio": st.column_config.NumberColumn(
            "Prezzo Pizza in Media (€)",
            format="%.2f",
            width=100,
            help="Prezzo medio delle pizze"
        ),
        "weekly_reviews": st.column_config.BarChartColumn(
            "Andamento Recensioni Settimanali",
            y_min=0,
            help="Numero recensioni giornaliere per l’ultima settimana"
        ),
        "distance_from_you": st.column_config.NumberColumn(
            "Distanza da te",
            format="%.2f km",
            width=120,
            help="Distanza della pizzeria da te in chilometri"
        )
    },
    hide_index=True,
    height=400
)

st.divider()

st.subheader("Pizzerie in evidenza")
st.write("Scopri chi sono le pizzerie più apprezzate, quelle con le recensioni peggiori e quelle in crescita nella tua zona:")

tab_migliore, tab_peggiore, tab_di_moda = st.tabs([" 🏆 La più apprezzata ", "  👎 La meno amata  ", "  📈 Di Moda "])

def render_review_tab(pizzeria_data, tab_type):
    """Helper function to render review tabs (migliore, peggiore, di moda)"""
    st.subheader(f"*{pizzeria_data['name'].iloc[0]}*")
    col1, col2 = st.columns([1.35, 4.1])
    
    with col1:
        st.metric(
            "**Rating Generale**", 
            f"{pizzeria_data['rating'].iloc[0]} ⭐️", 
            f"{pizzeria_data['rating_trend_su_mese'].iloc[0]} su mese", 
            border=True
        )
        
        changes = list(rng(4).standard_normal(20))
        st.metric(
            "**Recensioni Ricevute**", 
            pizzeria_data['total_reviews'].iloc[0], 
            f"{pizzeria_data['total_reviews_trend_su_mese'].iloc[0]}  su mese",
            chart_data=[sum(changes[:i]) for i in range(20)], 
            chart_type="line",
            border=True
        )
    
    with col2:
        st.write("Recensioni recenti:")
        with st.container(height=322, border=False):
            for comment in pizzeria_data['top_comments'].iloc[0]:
                with st.container(border=False):
                    source = "Google" if comment['rating'] > 3 else "TripAdvisor"  # Example logic
                    if(tab_type!="PEGGIOORE"):
                        st.success(
                            f":small[***{comment['author']} ({comment['date']})***  \n {source}]  \n"
                            f":small[*{comment['text']}*]  ↗"
                        )
                    else:
                        st.error(
                            f":small[***{comment['author']} ({comment['date']})***  \n {source}]  \n"
                            f":small[*{comment['text']}*]  ↗"
                        )

# Then replace the existing tab content with:
with tab_migliore:
    render_review_tab(best_pizzeria, 'MIGLIORE')

with tab_peggiore:
    render_review_tab(worst_pizzeria, 'PEGGIOORE')

with tab_di_moda:
    render_review_tab(trending_pizzeria, 'DI_MODA')
