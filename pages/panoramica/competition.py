import streamlit as st
import pydeck as pdk

from database.mock_data import competition_page_data
from pages.panoramica.utils.utils import map_generator

st.write("Competition Page")

# Nome della pizzeria dell'utente
name_of_my_pizzeria = "Pizzeria 4"

# Toggle settimana/mese
if "toggle_on" not in st.session_state:
    st.session_state.toggle_on = False
if "toggle_label" not in st.session_state:
    st.session_state.toggle_label = "Ultimi 7 giorni"
def update_label():
    if st.session_state.toggle_on:
        st.session_state.toggle_label = "Ultimi 30 giorni"
    else:
        st.session_state.toggle_label = "Ultimi 7 giorni"
st.toggle(
    st.session_state.toggle_label,
    key="toggle_on",
    on_change=update_label,
)

# Genera e mostra la mappa
map = map_generator(name_of_my_pizzeria, competition_page_data, st.session_state.toggle_on)
st.pydeck_chart(map)