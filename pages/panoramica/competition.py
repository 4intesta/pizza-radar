import streamlit as st
import pydeck as pdk

from database.mock_data import competition_page_data
from pages.panoramica.components.utils import map_generator
from pages.panoramica.components.utils import table_generator
from pages.panoramica.components.utils import computation_of_historical_rankings

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

# Calcola ranking per tabella e linechart
competition_page_data = computation_of_historical_rankings(competition_page_data)

# Genera tabella
competition_page_for_table, columns_to_show, column_config = table_generator(competition_page_data, st.session_state.toggle_on)
st.dataframe(competition_page_for_table[columns_to_show], column_config=column_config)

# Genera linechart
#(si usa competition_page_data NON competition_page_for_table) 

#print(competition_page_data.head())
