import streamlit as st
import pydeck as pdk

# Page configuration
st.set_page_config(
    page_title="Streamlit Data App",
    page_icon="🗺️",
    layout="wide"
)

st.title("Streamlit Data App with Interactive Map")

# Sample GeoJSON data
regions_data = [
    {
        "type": "Feature",
        "properties": {"name": "Region A", "population": 50000},
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-10, 30], [10, 30], [10, 50], [-10, 50], [-10, 30]
            ]]
        }
    },
    {
        "type": "Feature",
        "properties": {"name": "Region B", "population": 75000},
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [20, 10], [40, 10], [40, 30], [20, 30], [20, 10]
            ]]
        }
    }
]

points_data = [
    {"name": "City A", "type": "Capital", "coordinates": [0, 40]},
    {"name": "City B", "type": "Major", "coordinates": [30, 20]},
    {"name": "City C", "type": "Minor", "coordinates": [-5, 35]}
]

# Sidebar for layer controls
st.sidebar.header("Layers")
show_regions = st.sidebar.checkbox("Regions", value=True)
show_points = st.sidebar.checkbox("Points of Interest", value=True)

# Define initial view state
view_state = pdk.ViewState(
    latitude=35,
    longitude=15,
    zoom=3,
    pitch=0,
)

# Create layers based on toggle state
layers = []

if show_regions:
    regions_layer = pdk.Layer(
        "GeoJsonLayer",
        regions_data,
        opacity=0.4,
        stroked=True,
        filled=True,
        extruded=False,
        wireframe=True,
        get_fill_color=[0, 136, 136, 100],
        get_line_color=[0, 136, 136],
        line_width_min_pixels=2,
        pickable=True,
    )
    layers.append(regions_layer)

if show_points:
    points_layer = pdk.Layer(
        "ScatterplotLayer",
        points_data,
        get_position="coordinates",
        get_radius=50000,
        get_fill_color=[255, 51, 0],
        get_line_color=[255, 255, 255],
        line_width_min_pixels=2,
        pickable=True,
    )
    layers.append(points_layer)

# Create PyDeck map with MapLibre style
# PyDeck now uses MapLibre GL JS - no API keys required
# Use built-in styles: 'light', 'dark', 'road', 'satellite'
deck = pdk.Deck(
    #map_style='light',  # Built-in style
    map_style='https://demotiles.maplibre.org/style.json',  # Custom MapLibre style URL
    initial_view_state=view_state,
    layers=layers,
    tooltip={
        "html": "<b>Name:</b> {name}<br/><b>Type:</b> {type}<br/><b>Population:</b> {population}",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }
)

# Display map in Streamlit
st.pydeck_chart(deck)
