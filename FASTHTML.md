# FastHTML Data App

A practical guide for creating a spatially-enabled data application using FastHTML and MapLibre GL JS.

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver
- Basic Python knowledge

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

```bash
uv init fasthtml_data_app
cd fasthtml_data_app
```

### Install Dependencies

```bash
uv add python-fasthtml
```

## About FastHTML and Mapping

[FastHTML](https://fastht.ml/) is a Python web framework for building HTML-first applications. It works well for MapLibre integration because you can render page structure in Python while keeping client-side map behavior in JavaScript.

**Key points:**
- Server-rendered HTML with minimal boilerplate
- Easy script and style injection from Python components
- Full control over MapLibre GL JS layer setup and interactions

## Features Implemented

### Data Layers

The example includes two layers:

1. **Regions Layer** - Polygon GeoJSON rendered as a fill + line layer
2. **Points Layer** - Point GeoJSON rendered as circle markers

### Layer Toggle Controls

The app provides:
- Two checkbox controls (regions and points)
- Instant client-side layer visibility updates
- No full page reload required

Implementation approach:
- FastHTML renders the controls and map container
- MapLibre JS initializes map and layers in the browser
- Checkbox `change` events call `setLayoutProperty(..., 'visibility', ...)`

## Run the Application

```bash
uv run python app.py
```

Open your browser to `http://localhost:5001`

## Project Structure

```text
fasthtml_data_app/
├── app.py              # Main application file
├── pyproject.toml      # Project metadata and dependencies
└── README.md           # Quick start guide
```

## Resources

- [FastHTML Documentation](https://fastht.ml/)
- [MapLibre GL JS Docs](https://maplibre.org/maplibre-gl-js/docs/)
- [uv Documentation](https://github.com/astral-sh/uv)
