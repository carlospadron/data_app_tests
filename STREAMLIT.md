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

## Mapping Options for Streamlit

Streamlit doesn't have native MapLibre GL support, but several libraries work well for interactive maps with custom vector tile backgrounds:

### Option 1: PyDeck - Built-in (Recommended)

[PyDeck](https://deckgl.readthedocs.io/) is built into Streamlit via `st.pydeck_chart`. It provides high-performance WebGL-powered visualizations using MapLibre GL JS for rendering. **No additional installation or API keys required.**

### Option 2: Streamlit-Folium (Best for Vector Tiles)

[Folium](https://python-visualization.github.io/folium/) with the [streamlit-folium](https://github.com/randyzwitch/streamlit-folium) component supports custom tile layers including Mapbox Vector Tiles.

```bash
uv add streamlit-folium folium
```

### Option 3: Plotly

[Plotly](https://plotly.com/python/maps/) supports Mapbox maps with custom styles and vector tiles.

```bash
uv add plotly
```

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

## Create a Basic Map with PyDeck (Built-in)

### Create app.py

The main application file `app.py` includes layers and controls:

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

## Alternative: Using Streamlit-Folium

If you need custom Mapbox Vector Tiles without an API key, use Folium. Create `app_folium.py`:

```python
import streamlit as st
import folium
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(
    page_title="Streamlit Data App",
    page_icon="🗺️",
    layout="wide"
)

st.title("Streamlit Data App with Interactive Map")

# Create a folium map with custom vector tiles
# Using MapLibre demo tiles as base
m = folium.Map(
    location=[0, 0],
    zoom_start=2,
    tiles=None,  # Don't use default tiles
)

# Add MapLibre/Mapbox vector tile layer
folium.TileLayer(
    tiles='https://demotiles.maplibre.org/tiles/{z}/{x}/{y}.pbf',
    attr='MapLibre',
    name='MapLibre Demo',
    overlay=False,
    control=True,
    show=True,
).add_to(m)

# Alternative: Use Mapbox style URL if you have an access token
# folium.TileLayer(
#     tiles='https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=YOUR_TOKEN',
#     attr='Mapbox',
#     name='Mapbox Streets',
# ).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Display map in Streamlit
st_data = st_folium(m, width=1200, height=600)

# Display clicked location
if st_data['last_clicked']:
    st.write(f"Last clicked coordinates: {st_data['last_clicked']}")
```

## Alternative: Using Plotly with Mapbox

Create `app_plotly.py`:

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Streamlit Data App - Plotly",
    layout="wide"
)

st.title("Streamlit Data App with Plotly")

# Create Plotly map with Mapbox
fig = go.Figure(go.Scattermapbox(
    mode='markers',
    lon=[0],
    lat=[0],
    marker={'size': 10}
))

fig.update_layout(
    mapbox={
        'style': "open-street-map",  # or use custom Mapbox style with token
        'center': {'lon': 0, 'lat': 0},
        'zoom': 2
    },
    margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.info("💡 For custom Mapbox styles, set mapbox.accesstoken in layout")
```

## Run the Application

Start the Streamlit development server:

```bash
uv run treamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
streamlit_data_app/
├── app.py              # Main application file
├── pyproject.toml      # Project metadata and dependencies (managed by uv)
├── uv.lock            # Locked dependencies (managed by uv)
└── .venv/             # Virtual environment (not in git)
```

## Additional Features

### Add Markers to the Map

Update `app.py` to add markers:

```python
import folium
from folium import Marker, Popup

# Add markers
folium.Marker(
    location=[51.5074, -0.1278],
    popup=Popup("London", show=True),
    tooltip="London",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

folium.Marker(
    location=[40.7128, -74.0060],
    popup=Popup("New York", show=True),
    tooltip="New York",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)
```

### Add Sidebar Controls

```python
# Add sidebar
with st.sidebar:
    st.header("Map Controls")
    
    zoom_level = st.slider("Zoom Level", 1, 18, 2)
    
    center_lat = st.number_input("Center Latitude", -90.0, 90.0, 0.0)
    center_lon = st.number_input("Center Longitude", -180.0, 180.0, 0.0)
    
    if st.button("Update Map"):
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_level,
        )
        # Add your tile layers and markers here
```

### Display Data Alongside Map

```python
import pandas as pd

# Create sample data
data = pd.DataFrame({
    'City': ['London', 'New York', 'Tokyo'],
    'Latitude': [51.5074, 40.7128, 35.6762],
    'Longitude': [-0.1278, -74.0060, 139.6503],
    'Population': [9000000, 8400000, 14000000]
})

# Display data table
st.subheader("City Data")
st.dataframe(data)

# Add markers from dataframe
for idx, row in data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
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
```

## Deployment

### Streamlit Community Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy

### Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

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
