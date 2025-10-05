import streamlit as st
import altair as alt
import pandas as pd
from dataclasses import dataclass


# -------------------------
# Preserve Session States
# -------------------------
for k, v in st.session_state.items():
    if k.startswith("card_checkbox"):
        try:
            st.session_state[k] = v
        except st.errors.StreamlitValueAssignmentNotAllowedError:
            pass  # skip any keys Streamlit doesn't allow reassignment for
 

# -------------------------
# Card component
# -------------------------
@dataclass
class ActionCard:
    id: str
    title: str
    description: str
    kpi_key: str
    increment: int

def card_generator(action_id: str, label: str, description: str, kpi_key: str, increment: int = 5):
    with st.expander(label):
        st.markdown(f":small[{description}]")
        st.checkbox(
            ":small[Fatto]",
            key=f"card_checkbox_{action_id}",
            #on_change=lambda *a: update_cookie(action_id),
            #value=cookie_manager_checkboxes.get(action_id),
            args=(kpi_key, increment, action_id)
        )

# -------------------------
# KPI component
# -------------------------
def kpi_plotter(title: str, help: str, initial_value: float, cards: list[ActionCard]):
    # filter cards with checkbox state True & calculate new kpi value
    filtered_cards = [card for card in cards if st.session_state.get(f"card_checkbox_{card.id}", False)]
    total_increment = sum(card.increment for card in filtered_cards)
    new_value = min(initial_value + total_increment / 100, 1.0)

    with st.container(border=True):
        if total_increment == 0:
            st.metric(title, f"{new_value * 100:.0f}%", "Implementa le azioni consigliate", delta_color="off", help=help)
        else:
            st.metric(title, f"{new_value * 100:.0f}%", f"con azioni consigliate: +{total_increment}%", help=help)
        st.progress(new_value)
       
        st.text("Azioni consigliate")
        with st.container(border=False, height=200):
            for card in cards:
                card_generator(
                    card.id,
                    card.title,
                    card.description,
                    kpi_key=card.kpi_key,
                    increment=card.increment
                )

# -------------------------
# Strengths & Weaknesses component
# -------------------------
def feedback_section(feedback_dict: dict, max_freq: int, color: str = "#27AE60"):
    """
    Crea una sezione con grafico a barre + lista recensioni.
    
    Args:
        feedback_dict (dict): Dizionario con chiavi = categorie (es. "Atmosfera"),
                              valori = lista di commenti (dict con autore, data, piattaforma, link, testo).
        max_freq (int): Valore massimo comune da usare per l'asse Y.
        color (str): Colore delle barre (default verde).
    """

    # Creiamo DataFrame con frequenza = numero commenti
    data = pd.DataFrame({
        "Categoria": list(feedback_dict.keys()),
        "Frequenza": [len(comments) for comments in feedback_dict.values()],
        "Commenti": list(feedback_dict.values())
    })
    data = data.sort_values(by="Frequenza", ascending=False).reset_index(drop=True)

    # Layout a due colonne
    col1, col2 = st.columns([2, 1.7])

    with col1:
        st.write("")
        st.write("")
        st.write("")
        chart = (
            #plotta solo i 3 valori più frequenti
            alt.Chart(data.head(3))
            .mark_bar(color=color)
            .encode(
                x=alt.X(
                    "Categoria:N",
                    sort="-y",
                    title="",
                    axis=alt.Axis(labelAngle=0, grid=False, labelFontSize=14)
                ),
                y=alt.Y(
                    "Frequenza:Q",
                    title="Numero recensioni inerenti",
                    scale=alt.Scale(domain=[0, max_freq]),
                    axis=alt.Axis(grid=False, labelFontSize=14, format="d", tickMinStep=1)
                ),
                tooltip=["Categoria", "Frequenza"]
            )
            .properties(height=300, padding={"left": 0, "top": 9, "right": 0, "bottom": 1})
        )
        st.altair_chart(chart, use_container_width=True)

    with col2:
        st.write("Recensioni recenti:")
        with st.container(border=False, height=305):
            for _, row in data.iterrows():
                with st.expander(f"{row['Categoria']} ({row['Frequenza']})"):
                    for comment in row["Commenti"]:
                        # Tronca autore se troppo lungo
                        autore = comment["autore"]
                        if len(autore) > 20:
                            autore = autore[:17] + "..."
                        if color == "#27AE60":
                            st.success(
                                f":small[***{autore} ({comment['data']})***  \n {comment['piattaforma']}]  \n"
                                f":small[*{comment['testo']}*]  [↗]({comment['link']})"
                            )
                        else:  # altro colore (es. rosso = punti di debolezza)
                            st.error(
                                f":small[***{autore}***  \n ({comment['data']}) {comment['piattaforma']}]  \n"
                                f":small[*{comment['testo']}*]  [↗]({comment['link']})"
                            )


# -------------------------
# MAIN APP
# -------------------------
st.title("Panoramica")
st.subheader("Performance Generale")
st.write("Qui puoi monitorare metriche chiave e consultare possibili azioni per migliorare l’esperienza dei clienti:")
col1, col2, col3 = st.columns([1, 1, 1], vertical_alignment="bottom")

# -------------------------
# MAIN KPIS
# -------------------------
with col1:
    kpi_plotter("**Definire l’identità 🎯**", "Quanto la tua visione coincide con quella dei clienti.", 0.9,
        cards=[
            ActionCard(id="id_1", title="Valorizza il locale", description="Gli utenti apprezzano l'atmosfera del tuo locale, condividi foto e storie che mettano in risalto questo aspetto.", kpi_key="allineamento_percezioni_kpi", increment=5)
    ])

with col2:
    kpi_plotter("**Farsi Conoscere 🌐**", "Quanto sei attivo e coinvolgente online.", 0.8,
        cards=[
            ActionCard(id="id_3", title="Rispondi a recensione", description="Su Google, rispondi alla [recensione di Mario Rossi](https://www.tripadvisor.it/ShowUserReviews-g670816-d2474842-r1021101637-Il_Barolino-Carpi_Province_of_Modena_Emilia_Romagna.html).", kpi_key="presenza_social_kpi", increment=5),
            ActionCard(id="id_4", title="Pubblica contenuto", description="Condividi un post o una storia sui social per mantenere alto l’engagement.", kpi_key="presenza_social_kpi", increment=5)
        ]
    )

with col3:
    kpi_plotter("**Trattenere i clienti 📊**", "Quanto la tua pizzeria si distingue per qualità e servizio.", 0.85,
        cards=[
            ActionCard(id="id_5", title="Servizio", description="Gli utenti segnalano ritardi nella consegna delle pizze, rivedi la logistica per migliorare i tempi.", kpi_key="performance_pizzeria_kpi", increment=5),
            ActionCard(id="id_6", title="Atmosfera", description="Gli utenti si lamentano del rumore eccessivo nel locale, considera di migliorare l'isolamento acustico.", kpi_key="performance_pizzeria_kpi", increment=5),
            ActionCard(id="id_7", title="Qualità ingredienti", description="Evidenzia l’uso di ingredienti freschi e di qualità per distinguerti dalla concorrenza.", kpi_key="performance_pizzeria_kpi", increment=5)
        ]
    )

st.divider()

# -------------------------
# STRENGTHS & WEAKNESSES
# -------------------------
st.subheader("Punti di Forza e Debolezza")
st.write("Qui puoi vedere le aree di forza e di miglioramento del tuo locale, basati sulle recensioni recenti dei clienti:")
tab_strength, tab_weakness = st.tabs(["Punti di Forza 💪", "Punti di Debolezza ⚠️"])

# Dati strengths
strengths = {
    "Atmosfera": [
        {"autore": "Luca Bassi", "data": "10 mag", "piattaforma": "Google", "link": "https://goo.gl/maps/123", "testo": "Il locale è molto accogliente e curato nei dettagli."},
        {"autore": "Maria Rossi", "data": "1 giu", "piattaforma": "Tripadvisor", "link": "https://tripadvisor.com/review/456", "testo": "Atmosfera calda e familiare, ideale per serate tra amici."}
    ],
    "Servizio": [
        {"autore": "Sara Mantovani", "data": "20 apr", "piattaforma": "Google", "link": "https://goo.gl/maps/456", "testo": "Il personale è sempre gentile e disponibile."},
        {"autore": "Andrea Fiori", "data": "18 mag", "piattaforma": "Tripadvisor", "link": "https://tripadvisor.com/review/789", "testo": "Servizio rapido anche nei momenti di maggiore affluenza."},
        {"autore": "Chiara Lugli", "data": "5 ago", "piattaforma": "Google", "link": "https://goo.gl/maps/999", "testo": "Camerieri sorridenti e attenti alle esigenze."},
        {"autore": "Giovanni Palmieri", "data": "1 set", "piattaforma": "Facebook", "link": "https://facebook.com/review/101", "testo": "Servizio molto rapido e professionale."}
    ],
    "Qualità ingredienti": [
        {"autore": "Marco Domenico", "data": "14 mar", "piattaforma": "Google", "link": "https://goo.gl/maps/321", "testo": "Le pizze hanno ingredienti freschi e genuini."},
        {"autore": "Elisa Grandi", "data": "23 giu", "piattaforma": "Tripadvisor", "link": "https://tripadvisor.com/review/654", "testo": "Si sente la qualità degli ingredienti in ogni morso."}
    ],
    "Prezzo": [
        {"autore": "Anna Schiavi", "data": "5 feb", "piattaforma": "Google", "link": "https://goo.gl/maps/654", "testo": "Ottimo rapporto qualità-prezzo."}
    ]
}

# Dati weaknesses
weaknesses = {
    "Tempi di attesa": [
        {"autore": "Francesca Longobardi", "data": "12 lug", "piattaforma": "Google", "link": "https://goo.gl/maps/888", "testo": "Troppa attesa per ricevere le pizze, soprattutto nel weekend."},
        {"autore": "Davide Colombo", "data": "2 ago", "piattaforma": "Tripadvisor", "link": "https://tripadvisor.com/review/222", "testo": "Siamo rimasti al tavolo quasi 40 minuti prima che arrivasse l’ordine."},
        {"autore": "Elena Moretti", "data": "15 set", "piattaforma": "Facebook", "link": "https://facebook.com/review/333", "testo": "Servizio lento rispetto alle aspettative."}
    ],
    "Rumorosità": [
        {"autore": "Stefano Bianchi", "data": "3 mag", "piattaforma": "Google", "link": "https://goo.gl/maps/777", "testo": "Troppo rumore in sala, difficile parlare con gli amici."},
        {"autore": "Giulia Romano", "data": "19 lug", "piattaforma": "Tripadvisor", "link": "https://tripadvisor.com/review/444", "testo": "L’acustica del locale non è delle migliori, molto chiasso nelle ore di punta."}
    ],
    "Varietà del menu": [
        {"autore": "Roberto Ferri", "data": "21 mar", "piattaforma": "Google", "link": "https://goo.gl/maps/111", "testo": "Menu poco vario, avrei gradito più alternative vegetariane."},
        {"autore": "Martina Neri", "data": "14 giu", "piattaforma": "Tripadvisor", "link": "https://tripadvisor.com/review/555", "testo": "Manca un po’ di originalità nelle proposte, troppo classico."}
    ],
    "Parcheggio": [
        {"autore": "Lorenzo Gatti", "data": "10 apr", "piattaforma": "Google", "link": "https://goo.gl/maps/999", "testo": "Difficile trovare parcheggio vicino al locale."}
    ]
}

# Calcolo del massimo globale
max_strength = max(len(v) for v in strengths.values())
max_weakness = max(len(v) for v in weaknesses.values())
max_freq = max(max_strength, max_weakness)

with tab_strength:
    feedback_section(strengths, max_freq=max_freq)

with tab_weakness:
    feedback_section(weaknesses, max_freq=max_freq, color="#E74C3C")

st.divider()
st.subheader("Chatta con PizzaRadar")
st.write("Qui puoi chattare con PizzaRadar per ricevere consigli personalizzati e risposte alle tue domande")
