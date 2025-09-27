import streamlit as st
import altair as alt
import pandas as pd


st.title("Performance Generale")
st.write("Qui puoi monitorare le metriche chiave che ti aiutano a migliorare l’esperienza dei clienti:")

def donut_chart(percentage: float):
    """
    Draw a donut chart with green = percentage and transparent for the remainder.
    Show percentage text in the center.
    """
    percentage = max(0, min(100, percentage))  # clamp to [0,100]

    # Data for donut (use RGBA for transparency)
    source = pd.DataFrame({
        "category": ["Completed", "Remaining"],
        "value": [percentage, 100 - percentage],
        "color": ["#27AE60", "rgba(0,0,0,0)"]   # transparent slice
    })

    donut = alt.Chart(source).mark_arc(
        innerRadius=50,
        outerRadius=75,
        stroke=None,
        tooltip=None
    ).encode(
        theta="value",
        color=alt.Color("color:N", scale=None, legend=None)
    )

    # Central text
    text_source = pd.DataFrame({"text": [f"{percentage:.0f}%"]})
    
    text = alt.Chart(text_source).mark_text(
        size=30,
        fontWeight="bold",
        color="#27AE60",
        tooltip=None
    ).encode(
        text="text:N"
    )

    # Combine and set properties at the layered chart level
    chart = (donut + text).properties(
        height=170,
        width=170,
        padding={"left": 0, "top": 0, "right": 0, "bottom": 0}
    )

    return chart

def card(action_id: str, label: str, formatted_text: str):
    with st.expander(label):
        st.markdown(":small[" + formatted_text + "]")
        checked = st.checkbox(":small[Fatto]", key=f"card_checkbox_{action_id}")
    return checked
        
        

col1, col2, col3 = st.columns([1, 1, 1], vertical_alignment="bottom")
with col1:
    with st.container(border=True):
        st.metric("**Allineamento Percezioni 🎯**", "", "", help="Quanto la tua visione coincide con quella dei clienti.")
        allineamento_percezioni_kpi = 95
        allineamento_percezioni_addon = 0
        st.altair_chart(donut_chart(allineamento_percezioni_kpi), use_container_width=True)
        st.text("Azioni consigliate")
        with st.container(border=False, height=200):
            card("id_1", "Valorizza il locale", "Gli utenti apprezzano l'atmosfera del tuo locale, condividi foto e storie che mettano in risalto questo aspetto.")

with col2:
    with st.container(border=True):
        st.metric("**Presenza Social 🌐**", "", "", help="Quanto sei attivo e coinvolgente online.")
        presenza_social_kpi = 50
        presenza_social_addon = 0
        st.altair_chart(donut_chart(presenza_social_kpi), use_container_width=True)
        st.text("Azioni consigliate")
        with st.container(border=False, height=200):
            card("id_3", "Rispondi a recensione", "Su Google, rispondi alla [recensione di Mario Rossi](https://www.tripadvisor.it/ShowUserReviews-g670816-d2474842-r1021101637-Il_Barolino-Carpi_Province_of_Modena_Emilia_Romagna.html).")
            card("id_4", "Rispondi a recensione", "Su Google, rispondi alla [recensione di Mario Rossi](https://www.tripadvisor.it/ShowUserReviews-g670816-d2474842-r1021101637-Il_Barolino-Carpi_Province_of_Modena_Emilia_Romagna.html).")

with col3:
    with st.container(border=True):
        st.metric("**Performance Pizzeria 📊**", "", "", help="Il giudizio complessivo dei clienti sul tuo locale")
        performance_pizzeria_kpi = 33
        performance_pizzeria_addon = 0
        st.altair_chart(donut_chart(performance_pizzeria_kpi), use_container_width=True)
        st.text("Azioni consigliate")
        with st.container(border=False, height=200):
            card("id_5", "Servizio", "Gli utenti segnalano ritardi nella consegna delle pizze, rivedi la logistica per migliorare i tempi.")
            card("id_6", "Atmosfera", "Gli utenti si lamentano del rumore eccessivo nel locale, considera di migliorare l'isolamento acustico.")
