# Dash Data App

A comprehensive guide for creating a spatially-enabled data application using Dash and Plotly.

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

Create a new directory for your Dash project:

```bash
uv init dash_data_app
cd dash_data_app
```

### Install Dependencies

Install Dash and Plotly using uv:

```bash
uv add dash plotly pandas
```

## About Dash and Mapping

[Dash](https://dash.plotly.com/) is a Python framework for building analytical web applications. It uses [Plotly](https://plotly.com/python/) for visualizations, which now uses **MapLibre GL JS** for map rendering (switched from Mapbox GL JS).

**Key Points:**
- Plotly uses MapLibre GL JS natively (no API keys required for basic use)
- Supports custom map styles and GeoJSON layers
- Open Street Map style works out of the box
- Compatible with MapLibre GL style specifications

## Features Implemented

### Data Layers

The application includes two data layers:

1. **Regions Layer** - Polygon features rendered as filled shapes with outlines
2. **Points of Interest Layer** - Scatter plot markers for cities

### Layer Toggle Controls

A control panel provides:
- Checkboxes to toggle each layer independently
- Real-time updates using Dash callbacks
- Hover tooltips showing feature properties

Implementation approach:
- Dash `dcc.Checklist` component for layer controls
- Callback decorator linking controls to map figure
- Conditional trace creation based on selected layers

## Create the Map Application

### Create app.py

```python
import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Dash Data App"

# Sample GeoJSON data
regions_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Region A", "population": 50000},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-10, 30], [10, 30], [10, 50], [-10, 50], [-10, 30]
                ]]
            }
        }
    ]
}

points_data = [
    {"name": "City A", "type": "Capital", "lat": 40, "lon": 0},
    {"name": "City B", "type": "Major", "lat": 20, "lon": 30}
]

# Layout with controls and map
app.layout = html.Div([
    html.H1("Dash Data App with Interactive Map"),
    
    html.Div([
        html.H3("Layers"),
        dcc.Checklist(
            id='layer-toggles',
            options=[
                {'label': ' Regions', 'value': 'regions'},
                {'label': ' Points of Interest', 'value': 'points'}
            ],
            value=['regions', 'points']
        )
    ]),
    
    dcc.Graph(id='map', style={'height': '85vh'})
])

@callback(
    Output('map', 'figure'),
    Input('layer-toggles', 'value')
)
def update_map(selected_layers):
    fig = go.Figure()
    
    # Add regions layer if selected
    if 'regions' in selected_layers:
        for feature in regions_data['features']:
            coords = feature['geometry']['coordinates'][0]
            lons = [c[0] for c in coords]
            lats = [c[1] for c in coords]
            
            fig.add_trace(go.Scattermapbox(
                mode='lines',
                lon=lons,
                lat=lats,
                fill='toself',
                fillcolor='rgba(0, 136, 136, 0.4)',
                line=dict(color='rgb(0, 136, 136)', width=2),
                name=feature['properties']['name']
            ))
    
    # Add points layer if selected
    if 'points' in selected_layers:
        lons = [p['lon'] for p in points_data]
        lats = [p['lat'] for p in points_data]
        names = [p['name'] for p in points_data]
        
        fig.add_trace(go.Scattermapbox(
            mode='markers',
            lon=lons,
            lat=lats,
            marker=dict(size=14, color='rgb(255, 51, 0)'),
            text=names,
            name='Points of Interest'
        ))
    
    # Update layout with map style
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=35, lon=15),
            zoom=3
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
```

## Run the Application

Start the Dash development server:

```bash
uv run python app.py
```

The app will open at `http://localhost:8050`

## Project Structure

```
dash_data_app/
├── app.py              # Main application file
├── pyproject.toml      # Project metadata and dependencies
├── uv.lock            # Locked dependencies
└── .venv/             # Virtual environment
```

## Dash Callbacks

Dash uses a reactive callback system:

```python
@callback(
    Output('component-id', 'property'),
    Input('input-id', 'property')
)
def update_function(input_value):
    # Process input and return output
    return output_value
```

Key concepts:
- **Output**: What gets updated
- **Input**: What triggers the update
- **State**: Additional data without triggering updates

## Additional Features

### Add More Map Layers

```python
# Add a heat map layer
fig.add_trace(go.Densitymapbox(
    lat=lats,
    lon=lons,
    z=values,
    radius=10,
    colorscale='Viridis'
))
```

### Add Data Tables

```python
from dash import dash_table
import pandas as pd

# In layout
dash_table.DataTable(
    id='data-table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    style_table={'overflowX': 'auto'}
)
```

### Add Multiple Pages

```python
from dash import page_container, page_registry

app.layout = html.Div([
    dcc.Location(id='url'),
    html.Div([
        dcc.Link('Home', href='/'),
        dcc.Link('Map', href='/map')
    ]),
    page_container
])
```

### Custom Map Styles with JSON

You can use any MapLibre GL style specification:

```python
# Custom MapLibre style URL
fig.update_layout(
    mapbox=dict(
        style='https://demotiles.maplibre.org/style.json',
        center=dict(lat=35, lon=15),
        zoom=3
    )
)

# Or use a local style.json file
import json

with open('style.json') as f:
    custom_style = json.load(f)

fig.update_layout(
    mapbox=dict(
        style=custom_style,
        center=dict(lat=35, lon=15),
        zoom=3
    )
)
```

## Dash vs Streamlit Comparison

| Feature | Dash | Streamlit |
|---------|------|-----------|
| **Map Library** | Plotly (MapLibre GL JS) | PyDeck (MapLibre GL JS) |
| **API Keys** | None required | None required |
| **Reactivity** | Callback decorators | Auto-refresh |
| **Layout Control** | HTML/CSS components | Simple Python functions |
| **Learning Curve** | Medium | Low |
| **Flexibility** | High | Medium |
| **Best For** | Custom dashboards | Rapid prototyping |

## Dependencies Management

```bash
# Install from existing project
uv sync

# Add new packages
uv add dash plotly pandas numpy

# Export for compatibility
uv pip compile pyproject.toml -o requirements.txt
```

## Deployment

### Dash on Cloud Platforms

Deploy to various platforms:

```bash
# Render, Railway, Heroku, etc.
# Procfile:
web: gunicorn app:server

# Install gunicorn
uv add gunicorn
```

### Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8050

CMD ["python", "app.py"]
```

Build and run:

```bash
docker build -t dash-data-app .
docker run -p 8050:8050 dash-data-app
```

## Alternative Map Styles

Plotly with MapLibre GL JS supports various map styles:

```python
# Open Street Map (default, no token needed)
fig.update_layout(
    mapbox=dict(
        style='open-street-map',
        center=dict(lat=35, lon=15),
        zoom=3
    )
)

# Other built-in styles
# 'white-bg', 'carto-positron', 'carto-darkmatter', 'stamen-terrain', 'stamen-toner', 'stamen-watercolor'

# Custom MapLibre style (JSON URL)
fig.update_layout(
    mapbox=dict(
        style='https://demotiles.maplibre.org/style.json',
        center=dict(lat=35, lon=15),
        zoom=3
    )
)
```

## Resources

- [Dash Documentation](https://dash.plotly.com/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Dash Community Forum](https://community.plotly.com/)
- [Plotly Mapbox Documentation](https://plotly.com/python/mapbox-layers/)
