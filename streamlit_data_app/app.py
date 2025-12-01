import streamlit as st
import pydeck as pdk

# Page configuration
st.set_page_config(
    page_title="Streamlit Data App",
    page_icon="🗺️",
    layout="wide"
)

st.title("Streamlit Data App with Interactive Map")

# Define initial view state
view_state = pdk.ViewState(
    latitude=0,
    longitude=0,
    zoom=2,
    pitch=0,
)

# Create PyDeck map with MapLibre style
# PyDeck now uses MapLibre GL JS - no API keys required
# Use built-in styles: 'light', 'dark', 'road', 'satellite'
deck = pdk.Deck(
    map_style='light',  # Built-in style
    initial_view_state=view_state,
    layers=[],  # Add data layers here
)

# Display map in Streamlit
st.pydeck_chart(deck)

st.info("💡 PyDeck uses MapLibre GL JS - no API keys required!")
