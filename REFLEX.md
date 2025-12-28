# Reflex Implementation Guide

## ⚠️ Test Result: FAILED

**Status:** Failed - Map integration not working  
**Date:** December 28, 2025

### Issues Encountered

1. **Script Execution Problem**: Scripts embedded via `rx.script()` or `rx.html()` do not execute reliably in the browser
2. **MapLibre GL Integration**: Unable to initialize MapLibre GL map despite multiple approaches:
   - Using `rx.script()` component
   - Using `rx.html()` with inline scripts
   - Using separate map component
   - Direct integration in index function
3. **No Console Output**: JavaScript code shows no signs of execution in browser console
4. **Limited Documentation**: Lack of clear examples for integrating third-party JavaScript libraries

### Attempted Solutions

- ✗ rx.script() with external and inline scripts
- ✗ rx.html() wrapper with script tags
- ✗ Component-based approach
- ✗ Direct inline scripts in index function
- ✗ Various initialization timings (setTimeout, DOMContentLoaded)

### Conclusion

Reflex may not be suitable for projects requiring complex third-party JavaScript library integration. The framework's React compilation layer appears to interfere with direct script execution, making it difficult to integrate libraries like MapLibre GL that require DOM manipulation and initialization.

---

## Overview

Reflex is a full-stack Python framework that compiles to React, allowing you to build web applications entirely in Python without writing JavaScript, HTML, or CSS.

## Installation & Setup

### 1. Create Project Structure

```bash
cd reflex_data_app
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Initialize Reflex

```bash
uv run reflex init
```

This creates the necessary configuration and asset directories.

### 4. Run Development Server

```bash
uv run reflex run
```

Access at `http://localhost:3000`

## Project Structure

```
reflex_data_app/
├── pyproject.toml              # Dependencies and project metadata
├── rxconfig.py                 # Reflex configuration (port, app name)
├── assets/                     # Static files (auto-created)
├── .web/                       # Compiled frontend (auto-generated)
└── reflex_data_app/
    ├── __init__.py
    └── reflex_data_app.py      # Main application file
```

## Key Components

### 1. Configuration (`rxconfig.py`)

```python
import reflex as rx

config = rx.Config(
    app_name="reflex_data_app",
    port=3000,
)
```

### 2. State Management

Reflex uses a `State` class to manage application state:

```python
class State(rx.State):
    """The app state."""
    regions_visible: bool = True
    points_visible: bool = True

    def toggle_regions(self):
        """Toggle regions layer visibility."""
        self.regions_visible = not self.regions_visible

    def toggle_points(self):
        """Toggle points layer visibility."""
        self.points_visible = not self.points_visible
```

**Key Features:**
- State variables are automatically reactive
- Methods can modify state
- State changes trigger UI updates
- Backend state syncs with frontend automatically

### 3. Component Structure

Components are pure Python functions that return Reflex elements:

```python
def layer_controls() -> rx.Component:
    """Create layer toggle controls."""
    return rx.box(
        rx.vstack(
            rx.heading("Layers", size="4"),
            rx.checkbox(
                "Regions",
                checked=State.regions_visible,
                on_change=State.toggle_regions,
            ),
            rx.checkbox(
                "Points of Interest",
                checked=State.points_visible,
                on_change=State.toggle_points,
            ),
            spacing="3",
        ),
        position="absolute",
        top="80px",
        left="20px",
        background="white",
        padding="15px",
        border_radius="4px",
        box_shadow="0 2px 4px rgba(0,0,0,0.3)",
        z_index="1000",
        min_width="200px",
    )
```

**Component Types:**
- `rx.box` - Container (like `<div>`)
- `rx.vstack` / `rx.hstack` - Vertical/horizontal stacks
- `rx.heading` - Headings
- `rx.checkbox` - Checkbox input
- `rx.button` - Button
- `rx.el.div` - Raw HTML element

### 4. MapLibre GL Integration

Since MapLibre GL is a JavaScript library, we embed it using scripts:

```python
def map_component() -> rx.Component:
    """Create the MapLibre GL map component."""
    return rx.el.div(
        rx.el.div(id="map"),
        # Load MapLibre GL library
        rx.script(src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"),
        rx.el.link(
            href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css",
            rel="stylesheet"
        ),
        # Initialize map
        rx.script("""
            let map;
            
            function initMap() {
                if (map) return;
                
                map = new maplibregl.Map({
                    container: 'map',
                    style: 'https://demotiles.maplibre.org/style.json',
                    center: [15, 35],
                    zoom: 3
                });
                
                // Add layers...
            }
            
            initMap();
        """),
        width="100%",
        height="100vh",
    )
```

### 5. State-JavaScript Communication

To update JavaScript based on Python state changes:

```python
rx.script(f"""
    setInterval(() => {{
        const regionsVisible = {State.regions_visible};
        const pointsVisible = {State.points_visible};
        updateLayerVisibility(regionsVisible, pointsVisible);
    }}, 100);
""")
```

This polls the state and updates map layer visibility.

### 6. Main Page and App

```python
def index() -> rx.Component:
    """The main page."""
    return rx.box(
        rx.heading("Reflex Data App with Interactive Map"),
        layer_controls(),
        map_component(),
    )

app = rx.App()
app.add_page(index)
```

## Development Workflow

1. **Edit Code**: Modify `reflex_data_app.py`
2. **Hot Reload**: Changes auto-reload in browser
3. **Check Console**: Backend logs show state changes
4. **Browser DevTools**: Frontend React app for debugging

## Styling

Reflex supports inline styles as keyword arguments:

```python
rx.box(
    background="white",
    padding="15px",
    border_radius="4px",
    box_shadow="0 2px 4px rgba(0,0,0,0.3)",
)
```

Or CSS classes:
```python
rx.el.style("""
    #map {
        width: 100%;
        height: 100vh;
    }
""")
```

## Data Flow

1. User clicks checkbox
2. `on_change` triggers `State.toggle_regions()`
3. State updates `regions_visible`
4. React re-renders UI
5. JavaScript polling detects state change
6. MapLibre GL updates layer visibility

## Advantages

- **Pure Python**: No JavaScript, HTML, or CSS required
- **Type-Safe**: Full Python type hints and IDE support
- **React Performance**: Compiles to optimized React
- **Full-Stack**: Backend and frontend in one codebase

## Challenges

- **JavaScript Integration**: External JS libraries require embedding scripts
- **State Polling**: JavaScript needs polling to detect state changes
- **Learning Curve**: Need to understand React concepts (components, state)
- **Newer Framework**: Smaller ecosystem and community

## Deployment

### Reflex Hosting (Easiest)
```bash
reflex deploy
```

### Docker
```bash
reflex export
docker build -t reflex-app .
docker run -p 3000:3000 reflex-app
```

### Manual
```bash
reflex export --frontend-only
# Deploy .web/_static to CDN
# Deploy backend with gunicorn
```

## Best Practices

1. **Keep State Simple**: Only store what's needed
2. **Component Composition**: Break UI into small components
3. **Event Handlers**: Use State methods for logic
4. **Type Hints**: Leverage Python typing for safety
5. **JavaScript Bridge**: Minimize embedded scripts when possible

## Comparison with Other Frameworks

| Aspect | Reflex | Streamlit | Dash |
|--------|--------|-----------|------|
| Language | Pure Python | Pure Python | Pure Python |
| Frontend | React | Custom | React (Plotly.js) |
| State | Class-based | Auto-rerun | Callbacks |
| Complexity | Medium | Low | Medium |
| Flexibility | High | Low | High |
| Learning Curve | Medium | Very Low | Medium |

## Resources

- [Reflex Documentation](https://reflex.dev/docs/)
- [Reflex GitHub](https://github.com/reflex-dev/reflex)
- [Component Library](https://reflex.dev/docs/library/)
- [Deployment Guide](https://reflex.dev/docs/hosting/deploy/)
