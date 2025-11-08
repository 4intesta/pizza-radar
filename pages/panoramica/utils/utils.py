import pydeck as pdk
import pandas as pd
import streamlit as st

def value_to_color(n):
    if n <= 3:
        # Red to Yellow
        t = (n - 1) / (3 - 1)
        r = 255
        g = int(0 + (255 - 0) * t)
        b = 0
    else:
        # Yellow to Green
        t = (n - 3) / (5 - 3)
        r = int(255 - (255 - 0) * t)
        g = 255
        b = 0
    return (r, g, b)

def value_to_size(value, min_val, max_val, min_size=25, max_size=80):
    """Linearly map review counts to circle sizes for visualization."""
    if max_val == min_val:
        return (min_size + max_size) / 2  # avoid division by zero
    return min_size + (value - min_val) / (max_val - min_val) * (max_size - min_size)

def map_generator(my_pizzeria: str, competition_page_data: pd.DataFrame, toggle_on: bool = False) -> pdk.Deck:
    if toggle_on:
        print("Mappa: ultimi 30 giorni")
        ratings = competition_page_data['Average Rating last 30 days']
        reviews = competition_page_data['Number of Reviews last 30 days']

        min_reviews, max_reviews = reviews.min(), reviews.max()

        competition_page_data['color'] = ratings.apply(value_to_color)
        competition_page_data['scaled_size'] = reviews.apply(lambda x: value_to_size(x, min_reviews, max_reviews))

    else:
        print("Mappa: ultimi 7 giorni")
        ratings = competition_page_data['Average Rating last 7 days']
        reviews = competition_page_data['Number of Reviews last 7 days']

        min_reviews, max_reviews = reviews.min(), reviews.max()

        competition_page_data['color'] = ratings.apply(value_to_color)
        competition_page_data['scaled_size'] = reviews.apply(lambda x: value_to_size(x, min_reviews, max_reviews))



    la_mia_pizzeria = competition_page_data[competition_page_data["Name"] == my_pizzeria]
    altre_pizzerie = competition_page_data[competition_page_data["Name"] != my_pizzeria]

    center_latitude = la_mia_pizzeria["Latitude"].iloc[0]
    center_longitude = la_mia_pizzeria["Longitude"].iloc[0]
    
    # Layer for my pizzeria
    my_pizzeria_layer = pdk.Layer(
    "ScatterplotLayer",
    data=la_mia_pizzeria,
    get_position='[Longitude, Latitude]',
    get_fill_color='color',
    get_radius='scaled_size',
    pickable=True,
    auto_highlight=True,
    ) 
    # Layer for my pizzeria
    my_pizzeria_marker = pdk.Layer(
    "ScatterplotLayer",
    data=la_mia_pizzeria,
    get_position='[Longitude, Latitude]',
    get_fill_color='black',
    opacity=0.8,
    get_radius= 20,
    ) 

    # Layer for competitors
    competitors_layer = pdk.Layer(
    "ScatterplotLayer",
    data=altre_pizzerie,
    get_position='[Longitude, Latitude]',
    get_fill_color='color',
    get_radius='scaled_size',
    opacity=0.6,
    pickable=True,
    auto_highlight=True,
    )

    # --- Define the view ---
    view_state = pdk.ViewState(
        latitude=center_latitude,
        longitude=center_longitude,
        zoom=14,
        pitch=0,
    )

    # --- Tooltip ---
    if toggle_on:
        tooltip = {"html": "<b>{Name}</b><br>Recensioni: {Number of Reviews last 30 days}</br>Valutazione media: {Average Rating last 30 days}"}
    else:
        tooltip = {"html": "<b>{Name}</b><br>Recensioni: {Number of Reviews last 7 days}</br>Valutazione media: {Average Rating last 7 days}"}

    map = pdk.Deck(
        layers=[competitors_layer, my_pizzeria_layer, my_pizzeria_marker],
        initial_view_state=view_state,
        map_style=None,
        tooltip=tooltip
    )

    return map
