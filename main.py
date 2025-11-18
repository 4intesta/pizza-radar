import streamlit as st

# ---------------------------------------
# Page Definitions
# ---------------------------------------
p1 = st.Page("pages/panoramica/competition.py", title="Panoramica zona", icon=":material/local_pizza:", url_path="pizzerie-in-zona")
p2 = st.Page("pages/analisi recensioni/coach.py", title="Coach", icon=":material/school:", url_path="coach")
p3 = st.Page("pages/metrics/your_metrics.py", title="Le tue metriche", icon=":material/search_insights:", url_path="le-tue-metriche")
p4 = st.Page("pages/metrics/compare.py", title="Confrontati con altre pizzerie", icon=":material/compare_arrows:", url_path="confrontati-con-altre-pizzerie")
p5 = st.Page("pages/altro/contact_us.py", title="Contattaci", icon=":material/mail:", url_path="contattaci")
p6 = st.Page("pages/altro/account.py", title="Il tuo account", icon=":material/person:", url_path="il-tuo-account")

# ---------------------------------------
# Streamlit Page Configurations
# ---------------------------------------
st.set_page_config(layout="wide")
st.write('<style>div.block-container{padding-top:4rem;}</style>', unsafe_allow_html=True)

def compute_logged_out_page():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.container()
    with col2:
        with st.container(border=False):
            st.title("Effettua l'accesso")
            st.write("Accedi alla piattaforma per monitorare il gradimento dei clienti, seguire le tendenze vincenti e ricevere consigli pratici dal coach.")
            if st.button("Accedi alla piattaforma", width="stretch", type="primary"):
                st.login("auth0")
            st.link_button("Scopri tutte le funzionalità", "https://competio.lovable.app/competio-pizzeria", width="stretch")
    with col3:
        st.container()


if not st.user.is_logged_in:
    compute_logged_out_page()
else:
    pg = st.navigation({
        "Panoramica": [p1],
        "Analisi recensioni": [p2],
        "Metriche": [p3, p4],
        "Altro": [p6, p5]
        }, position="top")
    pg.run()