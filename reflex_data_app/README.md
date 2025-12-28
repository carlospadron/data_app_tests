# Reflex Data App

This is a spatially-enabled data application built with Reflex and MapLibre GL.

## Features

- Interactive MapLibre GL map with custom tile style
- Two GeoJSON layers:
  - Regions (polygons with population data)
  - Points of Interest (cities)
- Layer toggle controls
- Interactive popups on click
- Responsive design

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Initialize Reflex:
```bash
uv run reflex init
```

3. Run the development server:
```bash
uv run reflex run
```

4. Open your browser to `http://localhost:3000`

## Project Structure

```
reflex_data_app/
├── pyproject.toml              # Project dependencies
├── rxconfig.py                 # Reflex configuration
└── reflex_data_app/
    ├── __init__.py
    └── reflex_data_app.py      # Main application with State and components
```

## How It Works

Reflex is a full-stack Python framework that compiles to React components. This app:

1. **State Management**: Uses Reflex `State` class to track layer visibility
2. **MapLibre Integration**: Embeds MapLibre GL using JavaScript in `rx.script` components
3. **Reactivity**: Reflex state changes trigger UI updates through React
4. **Components**: Pure Python functions returning Reflex components (no HTML/JSX)

## Key Concepts

### State Class
```python
class State(rx.State):
    regions_visible: bool = True
    points_visible: bool = True
    
    def toggle_regions(self):
        self.regions_visible = not self.regions_visible
```

### Component Functions
```python
def layer_controls() -> rx.Component:
    return rx.box(
        rx.checkbox(
            "Regions",
            checked=State.regions_visible,
            on_change=State.toggle_regions,
        ),
    )
```

### JavaScript Integration
Reflex allows embedding JavaScript for libraries like MapLibre GL:
```python
rx.script("""
    map = new maplibregl.Map({...});
""")
```

## Deployment

Reflex apps can be deployed to various platforms:

1. **Reflex Hosting**: `reflex deploy`
2. **Docker**: Build and run container
3. **VPS**: Run with gunicorn/uvicorn

## Comparison with Other Frameworks

**Advantages:**
- Pure Python (no JavaScript knowledge required)
- Type-safe with Python type hints
- React performance under the hood
- Good for Python developers wanting full-stack capabilities

**Considerations:**
- More complex than Streamlit for simple apps
- Newer framework with smaller ecosystem
- Requires understanding React concepts (state, components)
- JavaScript library integration requires embedded scripts

## Learn More

- [Reflex Documentation](https://reflex.dev/docs/)
- [MapLibre GL JS Documentation](https://maplibre.org/maplibre-gl-js/docs/)
