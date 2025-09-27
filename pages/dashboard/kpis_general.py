import streamlit as st
import altair as alt
import pandas as pd


# -------------------------
# Donut chart function
# -------------------------
def donut_chart(base_value: float, added_value: float):
    """Draw a donut chart with base (dark green), added (light green), and remaining (transparent)."""
    # Clamp values
    base_value = max(0, min(100, base_value))
    added_value = max(0, min(100 - base_value, added_value))  # ensure total ≤ 100

    # Data for the donut slices
    source = pd.DataFrame({
        "category": ["Base", "Added", "Remaining"],
        "value": [base_value, added_value, 100 - base_value - added_value],
        "color": ["#27AE60", "#6FCF97", "rgba(0,0,0,0)"]  # dark green, light green, transparent
    })

    # Donut (arc) layer
    donut = alt.Chart(source).mark_arc(
        innerRadius=50, outerRadius=75
    ).encode(
        theta="value",
        color=alt.Color("color:N", scale=None, legend=None)
    )

    # Center text layer
    total = base_value + added_value
    text_source = pd.DataFrame({"text": [f"{total:.0f}%"]})
    text = alt.Chart(text_source).mark_text(
        size=30, fontWeight="bold", color="#27AE60"
    ).encode(
        text="text:N"
    )

    return (donut + text).properties(width=170, height=170)


# -------------------------
# KPI state initialization
# -------------------------
def init_kpi_state(base_key: str, base_value: int):
    """Ensure both base and added KPI states exist."""
    if base_key not in st.session_state:
        st.session_state[base_key] = base_value
    if f"{base_key}_added" not in st.session_state:
        st.session_state[f"{base_key}_added"] = 0


# -------------------------
# KPI update callback
# -------------------------
def update_added(kpi_key: str, increment: int, action_id: str):
    """Update the 'added' KPI portion when a checkbox is toggled."""
    checked = st.session_state[f"card_checkbox_{action_id}"]

    if checked:
        st.session_state[f"{kpi_key}_added"] = min(
            100 - st.session_state[kpi_key],
            st.session_state[f"{kpi_key}_added"] + increment
        )
    else:
        st.session_state[f"{kpi_key}_added"] = max(
            0,
            st.session_state[f"{kpi_key}_added"] - increment
        )


# -------------------------
# Card component
# -------------------------
def card(action_id: str, label: str, description: str, kpi_key: str, increment: int = 5):
    """A card with expandable details and a checkbox."""
    with st.expander(label):
        st.markdown(f":small[{description}]")
        st.checkbox(
            ":small[Fatto]",
            key=f"card_checkbox_{action_id}",
            on_change=update_added,
            args=(kpi_key, increment, action_id)
        )


# -------------------------
# MAIN APP
# -------------------------
st.title("Panoramica")
st.subheader("Performance Generale")
st.write("Qui puoi monitorare metriche chiave e consultare possibili azioni per migliorare l’esperienza dei clienti:")
col1, col2, col3 = st.columns([1, 1, 1], vertical_alignment="bottom")

# --- COL1 ---
with col1:
    with st.container(border=True):
        st.metric("**Allineamento Percezioni 🎯**", "", "",
                  help="Quanto la tua visione coincide con quella dei clienti.")

        init_kpi_state("allineamento_percezioni_kpi", 95)

        st.altair_chart(
            donut_chart(
                st.session_state["allineamento_percezioni_kpi"],
                st.session_state["allineamento_percezioni_kpi_added"]
            ),
            use_container_width=True
        )

        st.text("Azioni consigliate")
        with st.container(border=False, height=150):
            card(
                action_id="id_1",
                label="Valorizza il locale",
                description="Gli utenti apprezzano l'atmosfera del tuo locale, condividi foto e storie che mettano in risalto questo aspetto.",
                kpi_key="allineamento_percezioni_kpi",
                increment=5
            )

# --- COL2 ---
with col2:
    with st.container(border=True):
        st.metric("**Presenza Social 🌐**", "", "",
                  help="Quanto sei attivo e coinvolgente online.")

        init_kpi_state("presenza_social_kpi", 50)

        st.altair_chart(
            donut_chart(
                st.session_state["presenza_social_kpi"],
                st.session_state["presenza_social_kpi_added"]
            ),
            use_container_width=True
        )

        st.text("Azioni consigliate")
        with st.container(border=False, height=150):
            card(
                "id_3",
                "Rispondi a recensione",
                "Su Google, rispondi alla [recensione di Mario Rossi](https://www.tripadvisor.it/ShowUserReviews-g670816-d2474842-r1021101637-Il_Barolino-Carpi_Province_of_Modena_Emilia_Romagna.html).",
                kpi_key="presenza_social_kpi",
                increment=5
            )
            card(
                "id_4",
                "Pubblica contenuto",
                "Condividi un post o una storia sui social per mantenere alto l’engagement.",
                kpi_key="presenza_social_kpi",
                increment=5
            )

# --- COL3 ---
with col3:
    with st.container(border=True):
        st.metric("**Performance Pizzeria 📊**", "", "",
                  help="Il giudizio complessivo dei clienti sul tuo locale")

        init_kpi_state("performance_pizzeria_kpi", 33)

        st.altair_chart(
            donut_chart(
                st.session_state["performance_pizzeria_kpi"],
                st.session_state["performance_pizzeria_kpi_added"]
            ),
            use_container_width=True
        )

        st.text("Azioni consigliate")
        with st.container(border=False, height=150):
            card(
                "id_5",
                "Servizio",
                "Gli utenti segnalano ritardi nella consegna delle pizze, rivedi la logistica per migliorare i tempi.",
                kpi_key="performance_pizzeria_kpi",
                increment=5
            )
            card(
                "id_6",
                "Atmosfera",
                "Gli utenti si lamentano del rumore eccessivo nel locale, considera di migliorare l'isolamento acustico.",
                kpi_key="performance_pizzeria_kpi",
                increment=5
            )
            card(
                "id_7",
                "Qualità ingredienti",
                "Evidenzia l’uso di ingredienti freschi e di qualità per distinguerti dalla concorrenza.",
                kpi_key="performance_pizzeria_kpi",
                increment=5
            )
st.divider()
st.subheader("Punti di Forza e Debolezza")
st.write("Qui puoi vedere i punti di forza e le aree di miglioramento del tuo locale, basati sulle recensioni dei clienti:")


st.divider()
st.subheader("Chatta con PizzaRadar")
st.write("Qui puoi chattare con PizzaRadar per ricevere consigli personalizzati e risposte alle tue domande")