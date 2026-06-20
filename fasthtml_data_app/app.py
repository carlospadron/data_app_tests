import json

from fasthtml.common import Div, H1, H3, Input, Label, Link, Script, Style, Title, fast_app, serve

REGIONS_DATA = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Region A", "population": 50000},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[-10, 30], [10, 30], [10, 50], [-10, 50], [-10, 30]]],
            },
        },
        {
            "type": "Feature",
            "properties": {"name": "Region B", "population": 75000},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[20, 10], [40, 10], [40, 30], [20, 30], [20, 10]]],
            },
        },
    ],
}

POINTS_DATA = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "City A", "type": "Capital"},
            "geometry": {"type": "Point", "coordinates": [0, 40]},
        },
        {
            "type": "Feature",
            "properties": {"name": "City B", "type": "Major"},
            "geometry": {"type": "Point", "coordinates": [30, 20]},
        },
        {
            "type": "Feature",
            "properties": {"name": "City C", "type": "Minor"},
            "geometry": {"type": "Point", "coordinates": [-5, 35]},
        },
    ],
}

app, rt = fast_app(
    hdrs=(
        Link(rel="stylesheet", href="https://unpkg.com/maplibre-gl@5.9.0/dist/maplibre-gl.css"),
        Style(
            """
            body { margin: 0; font-family: system-ui, sans-serif; }
            h1 { text-align: center; margin: 18px 0; }
            #map { width: 100%; height: calc(100vh - 72px); }
            #layer-controls {
                position: absolute;
                top: 90px;
                left: 20px;
                z-index: 1000;
                background: #fff;
                border-radius: 6px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
                padding: 14px;
                min-width: 220px;
            }
            #layer-controls h3 { margin: 0 0 10px; font-size: 1rem; }
            #layer-controls label {
                display: flex;
                align-items: center;
                gap: 8px;
                margin: 6px 0;
                font-size: 0.95rem;
            }
            """
        ),
    )
)


@rt("/")
def get():
    return (
        Title("FastHTML Data App"),
        H1("FastHTML Data App with Interactive Map"),
        Div(
            H3("Layers"),
            Label(Input(type="checkbox", id="toggle-regions", checked=True), "Regions"),
            Label(Input(type="checkbox", id="toggle-points", checked=True), "Points of Interest"),
            id="layer-controls",
        ),
        Div(id="map"),
        Script(src="https://unpkg.com/maplibre-gl@5.9.0/dist/maplibre-gl.js"),
        Script(
            f"""
            const regionsData = {json.dumps(REGIONS_DATA)};
            const pointsData = {json.dumps(POINTS_DATA)};

            const map = new maplibregl.Map({{
              container: 'map',
              style: 'https://demotiles.maplibre.org/style.json',
              center: [15, 35],
              zoom: 3
            }});

            map.addControl(new maplibregl.NavigationControl(), 'top-right');

            map.on('load', () => {{
              map.addSource('regions', {{ type: 'geojson', data: regionsData }});
              map.addLayer({{
                id: 'regions-fill',
                type: 'fill',
                source: 'regions',
                paint: {{
                  'fill-color': '#008888',
                  'fill-opacity': 0.35
                }}
              }});
              map.addLayer({{
                id: 'regions-line',
                type: 'line',
                source: 'regions',
                paint: {{
                  'line-color': '#006666',
                  'line-width': 2
                }}
              }});

              map.addSource('points', {{ type: 'geojson', data: pointsData }});
              map.addLayer({{
                id: 'points-layer',
                type: 'circle',
                source: 'points',
                paint: {{
                  'circle-radius': 7,
                  'circle-color': '#ff3300',
                  'circle-stroke-color': '#ffffff',
                  'circle-stroke-width': 1.5
                }}
              }});

              const setVisible = (layerId, visible) => {{
                map.setLayoutProperty(layerId, 'visibility', visible ? 'visible' : 'none');
              }};

              document.getElementById('toggle-regions').addEventListener('change', (event) => {{
                setVisible('regions-fill', event.target.checked);
                setVisible('regions-line', event.target.checked);
              }});

              document.getElementById('toggle-points').addEventListener('change', (event) => {{
                setVisible('points-layer', event.target.checked);
              }});
            }});
            """
        ),
    )


if __name__ == "__main__":
    serve()
