# Streamlit Data App

A comprehensive guide for creating a spatially-enabled data application using Streamlit and interactive mapping libraries.

## Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver
- Basic knowledge of Python

## Installation

### Install uv

If you don't have uv installed:

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### Create a New Project

Create a new directory for your Streamlit project:

```bash
uv init streamlit_data_app
cd streamlit_data_app
```

### Install Streamlit

Install Streamlit and mapping dependencies using uv:

```bash
uv add streamlit
```

## MapLibre GL Integration with PyDeck

Streamlit includes [PyDeck](https://deckgl.readthedocs.io/) via `st.pydeck_chart`, which provides high-performance WebGL-powered visualizations using **MapLibre GL JS** for rendering. 

**Key advantages:**
- Built into Streamlit (no additional dependencies)
- Uses MapLibre GL JS natively (no API keys required)
- High-performance rendering with WebGL
- Perfect for GeoJSON and vector data visualization
- Supports custom MapLibre styles

## Features Implemented

### GeoJSON Layers

The application includes two data layers:

1. **Regions Layer** - Uses PyDeck's `GeoJsonLayer` to render polygon features
2. **Points of Interest Layer** - Uses PyDeck's `ScatterplotLayer` for point data

### Layer Toggle Controls

Streamlit's sidebar provides:
- Checkbox widgets for each layer
- Real-time layer filtering based on user selection
- Automatic map rerendering when toggles change

Implementation approach:
- Layer data defined as Python lists/dictionaries
- Conditional layer creation based on checkbox state
- Streamlit's reactive programming model handles UI updates automatically

## Create the Map Application

### Create app.py

The main application file `app.py` with GeoJSON layers and controls:

```python
import streamlit as st
import pydeck as pdk

# Page configuration
st.set_page_config(
    page_title="Streamlit Data App",
    page_icon="🗺️",
    layout="wide"
)

st.title("Streamlit Data App with Interactive Map")

# Sample GeoJSON data for regions and points
# Sidebar controls for layer visibility
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
    # Add GeoJsonLayer
    pass
if show_points:
    # Add ScatterplotLayer
    pass

# Create PyDeck map with MapLibre style
# PyDeck now uses MapLibre GL JS - no API keys required
# Use built-in styles: 'light', 'dark', 'road', 'satellite'
deck = pdk.Deck(
    #map_style='light',  # Built-in style
    map_style='https://demotiles.maplibre.org/style.json',  # Custom MapLibre style URL
    initial_view_state=view_state,
    layers=[],  # Add data layers here
)

# Display map in Streamlit
st.pydeck_chart(deck)
```

## Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [PyDeck Documentation](https://deckgl.readthedocs.io/)
- [MapLibre GL JS](https://maplibre.org/maplibre-gl-js/docs/)
- [uv Documentation](https://github.com/astral-sh/uv)

## Run the Application

Start the Streamlit development server:

```bash
uv run streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Map State Preservation

Streamlit automatically preserves map viewport state (zoom, pan) between script reruns:
- User interactions persist even when layer toggles trigger reruns
- Only explicit changes to `initial_view_state` reset the map
- This is built into Streamlit's component state management (v1.12+)

## Project Structure

```
streamlit_data_app/
├── app.py              # Main application file
├── pyproore GeoJSON Layers

```python
# Add another layer
polygon_layer = pdk.Layer(
    "GeoJsonLayer",
    your_geojson_data,
    opacity=0.8,
    stroked=True,
    filled=True,
    extruded=True,
    get_elevation='properties.height',
    get_fill_color=[255, 140, 0],
    get_line_color=[255, 255, 255],
)

layers.append(polygon_layer)
```

### Add Interactive Tooltips

```python
deck = pdk.Deck(
    map_style='https://demotiles.maplibre.org/style.json',
    initial_view_state=view_state,
    layers=layers,
    tooltip={
        "html": "<b>Name:</b> {name}<br/><b>Type:</b> {type}<br/><b>Population:</b> {population}",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }
)
```

folium.Marker(
    location=[40.7128, -74.0060],
    popup=Popup("New York", show=True),
    tooltip="New York",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)
```

### Add Sidebar Controls

```python
# Add sidebarTables

```python
import pandas as pd

# Create dataframe from layer data
data = pd.DataFrame(points_data)
st.sidebar.dataframe(datacation=[row['Latitude'], row['Longitude']],
        popup=f"{row['City']}<br>Pop: {row['Population']:,}",
        tooltip=row['City']
    ).add_to(m)
```

### Add Circle Markers with Size

```python
folium.Circle(
    location=[51.5074, -0.1278],
    radius=50000,  # meters
    color='crimson',
    fill=True,
    fillColor='crimson',
    fillOpacity=0.5,
    popup='London'
).add_to(m)
```

## Dependencies Management

uv automatically manages dependencies in `pyproject.toml`. To install all dependencies from an existing project:

```bash
uv sync
```

To add multiple packages at once:

```bash
uv add streamlit folium streamlit-folium pandas
```

Or for PyDeck variant:
```bash
uv add streamlit pydeck pandas
```

To export dependencies for compatibility:
```bash
uv pip compile pyproject.toml -o requirements.txt
```:

```bash
# Install from existing project
uv sync

# Add new packages
uv add streamlit pydeck pandas

# Export for compatibility /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:

```bash
docker build -t streamlit-data-app .
docker run -p 8501:8501 streamlit-data-app
```

## Limitations & Considerations

### Read-Focused Architecture
- Streamlit reruns the entire script on user interaction
- Not ideal for frequent write operations to databases
- Better suited for data visualization and exploration
- For write-heavy apps, consider web frameworks instead

### Mapping Library Limitations
- No native MapLibre GL support (uses Folium, PyDeck, or Plotly)
- Folium: Good for basic maps, less performant for large datasets
- PyDeck: Better performance, uses MapLibre GL JS (no API keys required)
- Plotly: Good integration with Streamlit, requires token for Mapbox styles

### State Management
- Use `st.session_state` for maintaining state across reruns
- Complex interactivity may require workarounds

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [Streamlit-Folium](https://github.com/randyzwitch/streamlit-folium)
- [Folium Documentation](https://python-visualization.github.io/folium/)
- [PyDeck Documentation](https://deckgl.readthedocs.io/)
- [Plotly Maps](https://plotly.com/python/maps/)

## Next Steps

- Add data layers from CSV/database
- Implement filtering and search functionality
- Add geospatial analysis (buffering, intersections)
- Integrate with PostGIS or spatial databases
- Add charts and visualizations alongside map
- Implement data export functionality
