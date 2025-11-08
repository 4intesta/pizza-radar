import streamlit as st

# ---------------------------------------
# Page Definitions
# ---------------------------------------
p1 = st.Page("pages/panoramica/competition.py", title="Pizzerie in zona", icon=":material/leaderboard:", url_path="pizzerie-in-zona")
p2 = st.Page("pages/analisi recensioni/coach.py", title="Coach", icon=":material/school:", url_path="coach")
p3 = st.Page("pages/metrics/your_metrics.py", title="Le tue metriche", icon=":material/search_insights:", url_path="le-tue-metriche")
p4 = st.Page("pages/metrics/compare.py", title="Confrontati con altre pizzerie", icon=":material/compare_arrows:", url_path="confrontati-con-altre-pizzerie")
p5 = st.Page("pages/altro/who_we_are.py", title="Chi siamo", icon=":material/people_outline:", url_path="chi-siamo")
p6 = st.Page("pages/altro/contact_us.py", title="Contattaci", icon=":material/mail:", url_path="contattaci")
p7 = st.Page("pages/altro/account.py", title="Il tuo account", icon=":material/account_circle:", url_path="il-tuo-account")

# ---------------------------------------
# Streamlit Page Configurations
# ---------------------------------------
# Shortening stupid Streamlit top padding
st.write('<style>div.block-container{padding-top:4rem;}</style>', unsafe_allow_html=True)



if not st.user.is_logged_in:
    if st.button("Authenticate"):
        st.login("auth0")
else:
    pg = st.navigation({
        "Panoramica": [p1],
        "Analisi recensioni": [p2],
        "Metriche": [p3, p4],
        "Altro": [p7, p5, p6]
        }, position="top")
    pg.run()

st.json(st.user.to_dict())