import streamlit as st
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = "google_maps_scraper"
CLIENTS_COLLECTION = "clients"
RESTAURANTS_COLLECTION = "restaurants"

if not MONGO_URI:
    st.error("MONGODB_URI not found in environment variables.")
    st.stop()

@st.cache_resource
def get_collection(collection_name):
    client = MongoClient(MONGO_URI)
    return client[DB_NAME][collection_name]

def read_client_and_competitors():
    """
    Fetch a single client document, then search for each competitor's URL in the restaurants collection.
    """
    # Safely get client_id from Streamlit user session
    client_id = getattr(getattr(st, "user", None), "sub", None)
    if not client_id:
        st.error("No client_id found in user session.")
        return

    st.write(f"Fetching document for client_id: {client_id!r}")

    try:
        clients_col = get_collection(CLIENTS_COLLECTION)
        restaurants_col = get_collection(RESTAURANTS_COLLECTION)
    except Exception as e:
        st.error(f"Could not connect to DB: {e}")
        return

    # Fetch the client document
    try:
        client_doc = clients_col.find_one({"client_id": client_id})
        if not client_doc:
            st.info("No client document found for this client_id.")
            return
        st.write("Client document:")
        st.json(client_doc)
    except Exception as e:
        st.error(f"Error fetching client document: {e}")
        return

    # Fetch competitor data
    competitors = client_doc.get("competitors", [])
    if not competitors:
        st.info("No competitors found for this client.")
        return

    st.write(f"Found {len(competitors)} competitors. Searching restaurants collection...")

    for comp in competitors:
        url = comp.get("url")
        if not url:
            continue

        try:
            restaurant_doc = restaurants_col.find_one({"url": url})
            if restaurant_doc:
                st.write(f"Restaurant data for competitor URL: {url}")
                st.json(restaurant_doc)
            else:
                st.info(f"No restaurant found for URL: {url}")
        except Exception as e:
            st.error(f"Error fetching restaurant for URL {url}: {e}")

