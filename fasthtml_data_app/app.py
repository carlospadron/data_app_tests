import json

from fasthtml.common import Div, H1, H3, Input, Label, Link, NotStr, Script, Style, Title, fast_app, serve

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
            "id": 0,
            "properties": {"id": 0, "name": "City A", "type": "Capital"},
            "geometry": {"type": "Point", "coordinates": [0, 40]},
        },
        {
            "type": "Feature",
            "id": 1,
            "properties": {"id": 1, "name": "City B", "type": "Major"},
            "geometry": {"type": "Point", "coordinates": [30, 20]},
        },
        {
            "type": "Feature",
            "id": 2,
            "properties": {"id": 2, "name": "City C", "type": "Minor"},
            "geometry": {"type": "Point", "coordinates": [-5, 35]},
        },
    ],
}

POINT_ROWS = [
    {
        "id": feature["properties"]["id"],
        "name": feature["properties"]["name"],
        "type": feature["properties"]["type"],
        "lon": feature["geometry"]["coordinates"][0],
        "lat": feature["geometry"]["coordinates"][1],
    }
    for feature in POINTS_DATA["features"]
]

app, rt = fast_app(
    hdrs=(
        Link(rel="stylesheet", href="https://unpkg.com/maplibre-gl@5.9.0/dist/maplibre-gl.css"),
        Style(
            """
            *, *::before, *::after { box-sizing: border-box; }
            html, body { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; font-family: system-ui, sans-serif; }
            main { padding: 0 !important; max-width: none !important; width: 100% !important; height: 100% !important; }
            #app-shell { position: relative; width: 100vw; height: 100vh; overflow: hidden; }
            #top-bar {
              position: absolute;
              top: 0;
              left: 0;
              right: 0;
              height: 62px;
              display: flex;
              align-items: center;
              justify-content: center;
              background: rgba(255, 255, 255, 0.9);
              backdrop-filter: blur(6px);
              border-bottom: 1px solid rgba(148, 163, 184, 0.22);
              z-index: 1002;
            }
            #top-bar h1 { margin: 0; font-size: 1.2rem; line-height: 1; }
            #map-frame { position: absolute; top: 62px; left: 0; right: 0; bottom: 0; }
            #map { position: absolute; inset: 0; width: 100%; height: 100%; }
            #layer-controls {
                position: absolute;
                top: 80px;
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
            #table-controls {
              position: absolute;
              right: 20px;
              bottom: 20px;
              z-index: 1000;
              background: #fff;
              border-radius: 6px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
              padding: 12px;
              min-width: 330px;
            }
            #table-controls h3 { margin: 0 0 8px; font-size: 1rem; }
            #table-controls table {
              width: 100%;
              border-collapse: collapse;
              font-size: 0.85rem;
            }
            #table-controls th, #table-controls td {
              text-align: left;
              padding: 6px;
              border-bottom: 1px solid #f0f0f0;
            }
            #table-controls th { border-bottom: 1px solid #ddd; }
            #table-controls tbody tr { cursor: pointer; }
            #table-controls tbody tr.selected,
            #table-controls tbody tr.selected td { background: #fef3c7 !important; }
            @media (max-width: 900px) {
              #layer-controls {
                top: 74px;
                left: 10px;
                min-width: 190px;
              }
              #table-controls {
                right: 10px;
                left: 10px;
                bottom: 10px;
                min-width: unset;
              }
            }
            """
        ),
    )
)


@rt("/")
def get():
    return (
        Title("FastHTML Data App"),
        Div(
        Div(H1("FastHTML Data App with Interactive Map"), id="top-bar"),
            Div(
                H3("Layers"),
                Label(Input(type="checkbox", id="toggle-regions", checked=True), "Regions"),
                Label(Input(type="checkbox", id="toggle-points", checked=True), "Points of Interest"),
                id="layer-controls",
            ),
            Div(
                H3("Points Table"),
                Div(
                  NotStr(
                    f"""
                    <table id='points-table'>
                        <thead>
                            <tr><th>Name</th><th>Type</th><th>Coords</th></tr>
                        </thead>
                        <tbody>
                            {''.join([f"<tr data-point-id='{row['id']}'><td>{row['name']}</td><td>{row['type']}</td><td>{row['lat']:.1f}, {row['lon']:.1f}</td></tr>" for row in POINT_ROWS])}
                        </tbody>
                    </table>
                    """,
                  ),
                    id="points-table-wrapper",
                ),
                id="table-controls",
            ),
              Div(Div(id="map"), id="map-frame"),
              id="app-shell",
        ),
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

            const resizeMap = () => map.resize();
            window.addEventListener('resize', resizeMap);

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
                  'circle-radius': ['case', ['boolean', ['feature-state', 'selected'], false], 14, 10],
                  'circle-color': ['case', ['boolean', ['feature-state', 'selected'], false], '#facc15', '#ff3300'],
                  'circle-stroke-color': '#ffffff',
                  'circle-stroke-width': ['case', ['boolean', ['feature-state', 'selected'], false], 3, 1.5]
                }}
              }});

              let selectedPointId = null;

              const syncSelectedPoint = (nextId) => {{
                if (selectedPointId !== null) {{
                  map.setFeatureState({{ source: 'points', id: selectedPointId }}, {{ selected: false }});
                }}
                if (nextId !== null) {{
                  map.setFeatureState({{ source: 'points', id: nextId }}, {{ selected: true }});
                }}
                selectedPointId = nextId;

                document.querySelectorAll('#points-table tbody tr[data-point-id]').forEach((row) => {{
                  const rowId = Number(row.getAttribute('data-point-id'));
                  if (nextId !== null && rowId === nextId) {{
                    row.classList.add('selected');
                    row.scrollIntoView({{ block: 'nearest' }});
                  }} else {{
                    row.classList.remove('selected');
                  }}
                }});
              }};

              const focusPoint = (pointId) => {{
                const feature = pointsData.features.find((item) => item.properties.id === pointId);
                if (!feature) return;
                map.flyTo({{ center: feature.geometry.coordinates, zoom: 5, essential: true }});
                syncSelectedPoint(pointId);
              }};

              map.on('click', (event) => {{
                const tolerancePx = 24;
                const maxDistSq = tolerancePx * tolerancePx;
                let nearestId = null;
                let nearestDistSq = Number.POSITIVE_INFINITY;

                for (const feature of pointsData.features) {{
                  const [lon, lat] = feature.geometry.coordinates;
                  const projected = map.project([lon, lat]);
                  const dx = projected.x - event.point.x;
                  const dy = projected.y - event.point.y;
                  const distSq = dx * dx + dy * dy;

                  if (distSq < nearestDistSq) {{
                    nearestDistSq = distSq;
                    nearestId = Number(feature.properties.id);
                  }}
                }}

                if (nearestId !== null && nearestDistSq <= maxDistSq) {{
                  focusPoint(nearestId);
                }}
              }});

              map.on('mouseenter', 'points-layer', () => {{
                map.getCanvas().style.cursor = 'pointer';
              }});

              map.on('mouseleave', 'points-layer', () => {{
                map.getCanvas().style.cursor = '';
              }});

              document.querySelectorAll('#points-table tbody tr[data-point-id]').forEach((row) => {{
                row.addEventListener('click', () => {{
                  const pointId = Number(row.getAttribute('data-point-id'));
                  if (!Number.isNaN(pointId)) {{
                    focusPoint(pointId);
                  }}
                }});
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

              // Ensure map canvas aligns with final layout after controls mount.
              requestAnimationFrame(() => map.resize());
              setTimeout(() => map.resize(), 120);
            }});
            """
        ),
    )


if __name__ == "__main__":
    serve()
