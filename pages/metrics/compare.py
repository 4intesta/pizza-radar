import streamlit as st

from database.mock_data import competition_page_data
from pages.metrics.components.utils import pizza_price_selector
from pages.metrics.components.utils import menu_items
from pages.metrics.components.utils import gradimento
from pages.metrics.components.utils import computation_of_historical_gradimento
from pages.metrics.components.utils import render_comparison_tab
from pages.metrics.components.utils import render_platform

competition_page_data = computation_of_historical_gradimento(competition_page_data)

name_of_my_pizzeria = "Pizzeria 4"

st.subheader("Confronta la tua Pizzeria con altre in zona")
st.write("Scegli una pizzeria in zona e scopri la sua performance rispetto alla tua:")

# Store selectbox value in a variable
selected_pizzeria = st.selectbox(
    "Confronta la tua pizzera con altre in zona", 
    options=competition_page_data[competition_page_data['Name'] != name_of_my_pizzeria]['Name'].tolist(), 
    index=None,
    placeholder="Scegli una pizzeria in zona...", 
    label_visibility="collapsed"
)

if selected_pizzeria:

    competitor_data = competition_page_data.loc[competition_page_data['Name'] == selected_pizzeria].iloc[0]
    my_data = competition_page_data.loc[competition_page_data['Name'] == name_of_my_pizzeria].iloc[0]

    col1, col2, col3 = st.columns([2.0, 2.7, 1.5])
    with col1:
        pizza_price_selector(my_data, competitor_data)
        menu_items(my_data, competitor_data)
        
    with col2:
        gradimento(my_data, competitor_data)

    with col3:
        render_platform(my_data, competitor_data)

    tab_comparison_general, tab_comparison_cibo, tab_comparison_servizio, tab_comparison_atmosfera, tab_comparison_qualita_prezzo = st.tabs([
        "Generale :material/star:",
        "Cibo :material/local_pizza:", 
        "Servizio :material/hand_meal:", 
        "Atmosfera :material/candle:", 
        "Qualità/Prezzo :material/money_bag:"
    ])
    
    with tab_comparison_general:
        render_comparison_tab(name_of_my_pizzeria, competition_page_data, selected_pizzeria, 'Generale')        
    with tab_comparison_cibo:
        render_comparison_tab(name_of_my_pizzeria, competition_page_data, selected_pizzeria, 'Cibo')
        
    with tab_comparison_servizio:
        render_comparison_tab(name_of_my_pizzeria, competition_page_data, selected_pizzeria, 'Servizio')
        
    with tab_comparison_atmosfera:
        render_comparison_tab(name_of_my_pizzeria, competition_page_data, selected_pizzeria, 'Atmosfera')
        
    with tab_comparison_qualita_prezzo:
        render_comparison_tab(name_of_my_pizzeria, competition_page_data, selected_pizzeria, 'Qualità/Prezzo')
