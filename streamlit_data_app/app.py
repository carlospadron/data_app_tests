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
    {"id": 0, "name": "City A", "type": "Capital", "coordinates": [0, 40]},
    {"id": 1, "name": "City B", "type": "Major", "coordinates": [30, 20]},
    {"id": 2, "name": "City C", "type": "Minor", "coordinates": [-5, 35]}
]

if "selected_point_id" not in st.session_state:
    st.session_state.selected_point_id = None

# Sidebar for layer controls
st.sidebar.header("Layers")
show_regions = st.sidebar.checkbox("Regions", value=True)
show_points = st.sidebar.checkbox("Points of Interest", value=True)

point_lookup = {point["name"]: point for point in points_data}
selected_name = st.sidebar.selectbox(
    "Focus point from table",
    ["None"] + [point["name"] for point in points_data],
    index=0 if st.session_state.selected_point_id is None else st.session_state.selected_point_id + 1,
)

if selected_name != "None":
    selected_point = point_lookup[selected_name]
    st.session_state.selected_point_id = selected_point["id"]
else:
    selected_point = None
    st.session_state.selected_point_id = None

# Define initial view state
view_state = pdk.ViewState(
    latitude=selected_point["coordinates"][1] if selected_point else 35,
    longitude=selected_point["coordinates"][0] if selected_point else 15,
    zoom=5 if selected_point else 3,
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
    points_layer_data = []
    for point in points_data:
        is_selected = point["id"] == st.session_state.selected_point_id
        points_layer_data.append(
            {
                **point,
                "color": [250, 204, 21] if is_selected else [255, 51, 0],
                "radius": 80000 if is_selected else 50000,
            }
        )

    points_layer = pdk.Layer(
        "ScatterplotLayer",
        points_layer_data,
        get_position="coordinates",
        get_radius="radius",
        get_fill_color="color",
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

st.subheader("Points Table")
table_rows = [
    {
        "Name": point["name"],
        "Type": point["type"],
        "Coordinates": f"{point['coordinates'][1]:.1f}, {point['coordinates'][0]:.1f}",
        "Selected": point["id"] == st.session_state.selected_point_id,
    }
    for point in points_data
]
st.dataframe(table_rows, use_container_width=True, hide_index=True)
