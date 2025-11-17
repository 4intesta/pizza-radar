import streamlit as st

from database.mock_data import competition_page_data
from pages.panoramica.components.utils import map_generator
from pages.panoramica.components.utils import table_generator
from pages.panoramica.components.utils import computation_of_historical_rankings
from pages.panoramica.components.utils import linechart_generator
from pages.panoramica.components.utils import render_review_tab
from pages.panoramica.components.utils import get_best_last_7d
from pages.panoramica.components.utils import get_worst_last_7d

# Nome della pizzeria dell'utente
name_of_my_pizzeria = "Pizzeria 4"

st.title("Panoramica zona")
st.markdown("Il modulo **Panoramica zona** mostra il :primary-background[gradimento percepito] della tua pizzeria e delle altre in zona, evidenziando trend di gradimento e fattori che li influenzano.  \n Questa vista permette di comprendere rapidamente cosa accade intorno a te e quali aspetti i clienti valorizzano o criticano maggiormente.")

st.header("Percezione attuale")
st.write("La sezione **Percezione attuale** mostra la percezione recente tua pizzeria e delle altre in zona tramite mappa o tabella. Usa il toggle per visionare i dati degli ultimi 7 o 30 giorni.")

# Toggle Percezione attuale settimana/mese
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

tab_map, tab_table, = st.tabs(["Mappa della zona :material/map:", "Vista Tabellare :material/table:"])
with tab_map:
    map = map_generator(name_of_my_pizzeria, competition_page_data, st.session_state.toggle_on)
    st.pydeck_chart(map)

competition_page_data = computation_of_historical_rankings(competition_page_data)
with tab_table:
    competition_page_for_table, columns_to_show, column_config = table_generator(competition_page_data, st.session_state.toggle_on)
    st.dataframe(competition_page_for_table[columns_to_show], column_config=column_config, height=500)

st.divider()
st.header("Percezione storica")
st.write("La sezione **Percezione storica** visualizza il trend dell’ultimo anno della tua pizzeria e delle altre in zona tramite diagramma. Confronta più pizzerie selezionandole dal menu a tendina.")

# Toggle Percezione storica settimana/mese
if "historical_toggle_on" not in st.session_state:
    st.session_state.historical_toggle_on = False
if "historical_toggle_label" not in st.session_state:
    st.session_state.historical_toggle_label = "Percezione storica: ultimi 7 giorni"

def update_historical_label():
    if st.session_state.historical_toggle_on:
        st.session_state.historical_toggle_label = "Ultimo mese"
    else:
        st.session_state.historical_toggle_label = "Ultimo anno"

st.toggle(
    st.session_state.historical_toggle_label,
    key="historical_toggle_on",
    on_change=update_historical_label,
)

competition_page_for_linechart = linechart_generator(competition_page_data, name_of_my_pizzeria, st.session_state.historical_toggle_on)
st.altair_chart(competition_page_for_linechart, use_container_width=True)

st.divider()
st.header("In evidenza")
st.write("La sezione **In evidenza** mostra le pizzerie che si sono contraddistinte negli ultimi 7 giorni.")

tab_la_tua, tab_migliore, tab_peggiore = st.tabs(["La tua :material/person:", "La più apprezzata :material/crown:", " La meno amata :material/heart_broken:"])
avg_eviews_rating_last_7_days = competition_page_data["Average Rating last 7 days"].mean()
avg_reviews_number_7_days = competition_page_data["Number of Reviews last 7 days"].mean()
with tab_la_tua:
    render_review_tab(competition_page_data.loc[competition_page_data["Name"] == name_of_my_pizzeria], avg_eviews_rating_last_7_days, avg_reviews_number_7_days)
with tab_migliore:
    best_pizzeria = get_best_last_7d(competition_page_for_table)
    render_review_tab(competition_page_data.loc[competition_page_data["Name"] == best_pizzeria], avg_eviews_rating_last_7_days, avg_reviews_number_7_days)
with tab_peggiore:
    worst_pizzeria = get_worst_last_7d(competition_page_for_table)
    render_review_tab(competition_page_data.loc[competition_page_data["Name"] == worst_pizzeria], avg_eviews_rating_last_7_days, avg_reviews_number_7_days)