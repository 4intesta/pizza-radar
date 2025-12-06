import streamlit as st

from database.mock_data import competition_page_data
from pages.metrics.components.utils import render_prices_diagram
from pages.metrics.components.utils import render_menu_items_and_stay_and_wait
from pages.metrics.components.utils import render_general_ratings
from pages.metrics.components.utils import render_comment_diagram
from pages.metrics.components.utils import render_comment_linechart
from pages.metrics.components.utils import render_subcategory_tab


st.subheader("La tua Offerta")
#st.write("Confronta i tuoi prezzi e le metriche chiave con quelli delle pizzerie concorrenti in zona:")

name_of_my_pizzeria = "Pizzeria 4"

colprices, colmenu = st.columns([4.1, 1.35], vertical_alignment="bottom")
with colprices:
    render_prices_diagram(competition_page_data, name_of_my_pizzeria)

with colmenu:
    render_menu_items_and_stay_and_wait(competition_page_data, name_of_my_pizzeria)
    

st.divider()

st.subheader("Recensioni e Valutazioni")

col1, col2, col3 = st.columns([1.35, 1.8, 2.3], vertical_alignment="bottom")

with col1:
    render_general_ratings(competition_page_data, name_of_my_pizzeria)

with col2:
    render_comment_diagram(competition_page_data, name_of_my_pizzeria)

with col3:
    render_comment_linechart(competition_page_data, name_of_my_pizzeria)


tab_general, tab_food, tab_service, tab_ambience, tab_quality_price = st.tabs([
        "Generale :material/star:",
        "Cibo :material/local_pizza:", 
        "Servizio :material/hand_meal:", 
        "Atmosfera :material/candle:", 
        "Qualità/Prezzo :material/money_bag:"
    ])

with tab_general:
    render_subcategory_tab(competition_page_data, name_of_my_pizzeria, "rating_generale", "Generale")

with tab_food:
    render_subcategory_tab(competition_page_data, name_of_my_pizzeria, "rating_cibo", "Cibo")

with tab_service:
    render_subcategory_tab(competition_page_data, name_of_my_pizzeria, "rating_servizio", "Servizio")

with tab_ambience:
    render_subcategory_tab(competition_page_data, name_of_my_pizzeria, "rating_atmosfera", "Atmosfera")

with tab_quality_price:
    render_subcategory_tab(competition_page_data, name_of_my_pizzeria, "rating_qualita_prezzo", "Qualità/Prezzo")