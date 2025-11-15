import streamlit as st

from database.mock_data import competition_page_data
from pages.panoramica.components.utils import map_generator
from pages.panoramica.components.utils import table_generator
from pages.panoramica.components.utils import computation_of_historical_rankings
from pages.panoramica.components.utils import linechart_generator

st.title("Percezione nella tua zona")
st.write("Osserva come la tua pizzeria si colloca rispetto alle realtà attorno a te. La mappa mostra i competitor più vicini, mentre la tabella – ordinata in base alle pizze più apprezzate – ti offre un confronto immediato e intuitivo. Un insight chiaro per capire trend e opportunità.")

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

# MAPPA
map = map_generator(name_of_my_pizzeria, competition_page_data, st.session_state.toggle_on)
st.pydeck_chart(map)

tab_table, tab_line_chart, = st.tabs(["Vista Tabellare :material/table:", "Vista Storica :material/moving:"])
competition_page_data = computation_of_historical_rankings(competition_page_data)
with tab_table:
    #TODO: Aggiungerei colonna "cosa va bene/male"
    competition_page_for_table, columns_to_show, column_config = table_generator(competition_page_data, st.session_state.toggle_on)
    st.dataframe(competition_page_for_table[columns_to_show], column_config=column_config)

with tab_line_chart:
    competition_page_for_linechart = linechart_generator(competition_page_data, name_of_my_pizzeria)
    st.altair_chart(competition_page_for_linechart, use_container_width=True)
