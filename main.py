import streamlit as st
import os, base64
from numpy.random import default_rng as rng
import streamlit_authenticator as stauth

# -------------------------
# Utility Functions
# -------------------------
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

# -------------------------
# Preserve Session States
# -------------------------
for k, v in st.session_state.items():
    if k.startswith("card_checkbox"):
        try:
            st.session_state[k] = v
        except st.errors.StreamlitValueAssignmentNotAllowedError:
            pass
        
##narrow screen blocker
def small_screen_blocker():
    # Load image
    img_base64 = get_img_as_base64("warning.jpeg")

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
# Define your users
credentials = {
    "usernames": {
        "user1": {
            "name": "User One",
            "password": "password1"
        },
        "user2": {
            "name": "User Two",
            "password": "password2"
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    'your_app_name',
    'your_cookie_name',
    cookie_expiry_days=30
)
# Store the authenticator object in the session state
st.session_state["authenticator"] = authenticator

#controlla se authentication_status è True o se ci sono cookie di login
if st.session_state["authentication_status"] or authenticator.cookie_controller.get_cookie() is not None:
    st.session_state["authentication_status"] = True
    main_content()
else:
    col1, col2 = st.columns([1, 1])
    
    # Add custom CSS for columns and form
    st.markdown("""
        <style>
            [data-testid="stForm"] {
                border: none;
                padding: 0;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            /* Make columns equal height */
            [data-testid="column"] {
                height: calc(100vh - 100px);
                display: flex;
                align-items: center;
            }
            /* Remove default form padding */
            .stButton {
                margin-top: 1rem;
            }
            /* Center form elements */
            [data-testid="stVerticalBlock"] {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)
    
    with col1:
        login_img = get_img_as_base64("Login1.jpeg")
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                <img src="data:image/jpeg;base64,{login_img}" 
                     style="max-width: 100%; height: auto; border-radius: 8px;"
                     alt="Login Image">
            </div>
        """, unsafe_allow_html=True)
    with col2:
        authenticator.login(key='Login', location='main')
        if st.session_state["authentication_status"] is False:
            st.error("Username/password is incorrect")