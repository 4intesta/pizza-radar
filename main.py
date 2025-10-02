import streamlit as st
import os, base64
from numpy.random import default_rng as rng

# -------------------------
# Preserve Session States
# -------------------------
for k, v in st.session_state.items():
    st.session_state[k] = v

##narrow screen blocker
def small_screen_blocker():
    def get_img_as_base64(file_name):
        try:
            # Prima prova il percorso relativo per Streamlit Cloud
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_paths = [
                os.path.join(current_dir, "assets", file_name),  # Percorso standard
                os.path.join(".", "assets", file_name),          # Percorso relativo
                os.path.join("assets", file_name),               # Percorso diretto
                os.path.join("pizza-radar","assets", file_name)
            ]
            
            for file_path in file_paths:
                if os.path.exists(file_path):
                    with open(file_path, "rb") as img_file:
                        return base64.b64encode(img_file.read()).decode()
            
            # Se siamo qui, stampa info di debug
            st.write("Debug - Percorsi tentati:")
            for path in file_paths:
                st.write(f"- {path} (exists: {os.path.exists(path)})")
            
            # Se non troviamo il file, usa un'immagine di fallback codificata direttamente
            return "iVBORw0KGgoAAAANSUhEUgAAAQAAAAEAAQMAAABmvDolAAAAA1BMVEX///+nxBvIAAAAAXRSTlMAQObYZgAAABxJREFUeNrtwTEBAAAAwqD1T20ND6AAAAAA4NcAEsAAAcw7WmwAAAAASUVORK5CYII="
            
        except Exception as e:
            st.error(f"Error loading image: {e}")
            return ""

    # Load image
    img_base64 = get_img_as_base64("warning.png")

    # CSS per il responsive design
    st.markdown(f"""
        <style>
            @media (max-width: 768px) and (orientation: portrait) {{
                .main .block-container {{ display: none !important; }}
                #mobile-warning {{ 
                    display: flex !important;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    padding: 20px;
                    text-align: center;
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: white;
                    z-index: 9999;
                }}
            }}
            @media (min-width: 641px), (orientation: landscape) {{
                #mobile-warning {{ display: none !important; }}
                .main .block-container {{ display: block !important; }}
            }}
            #mobile-warning img {{
                max-width: 80%;
                height: auto;
                margin-bottom: 20px;
                border-radius: 8px;
            }}
            #mobile-warning p {{
                font-size: 16px;
                color: #333;
                max-width: 80%;
                margin: 0 auto;
            }}
        </style>
        <div id="mobile-warning">
            <img src="data:image/jpeg;base64,{img_base64}" alt="Warning Image">
            <p>Schermo troppo piccolo, per experience migliore prova a ruotare lo schermo o connetterti da computer</p>
        </div>
    """, unsafe_allow_html=True)
#small_screen_blocker()

##hide streamlit menu
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
#st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#set page layout to wide
st.set_page_config(layout="wide")

# -------------------------
# Debugging
# -------------------------
#st.write(st.session_state)

# -------------------------
# MAIN PAGE CONTENT
# -------------------------
def main_content():
    nomePizzeria = "La Mia Pizzeria"

    pages = {
        "Dashboard  🍕": [
            st.Page("pages/dashboard/kpis_general.py", title="Panoramica"),
            st.Page("pages/dashboard/kpis_advanced.py", title="Approfondimento"),
        ],
        "Account 👤": [
            st.Page("pages/account/manage_account.py", title="Gestisci il tuo account"),
        ],
        "Altro  📪": [
            st.Page("pages/contacts/who_we_are.py", title="Chi siamo"),
            st.Page("pages/contacts/send_us_a_message.py", title="Contattaci"),
        ],
    }

    pg = st.navigation(pages, position="top")
    pg.run()

# -------------------------
# Login
# -------------------------
# Ensure the session state variable exists
if "user_logged" not in st.session_state:
    st.session_state["user_logged"] = False

# Case: user not logged in
if not st.session_state["user_logged"]:
    st.warning("⚠️ User not logged in.")
    st.write("Please log in to access the content.")

    if st.button("Log in"):
        st.session_state["user_logged"] = True
        st.rerun()

# Case: user logged in
else:
    main_content()
