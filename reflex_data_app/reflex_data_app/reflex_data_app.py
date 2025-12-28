"""Reflex data app with MapLibre GL integration."""
import reflex as rx


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
}

points_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "City A", "type": "Capital"},
            "geometry": {"type": "Point", "coordinates": [0, 40]}
        },
        {
            "type": "Feature",
            "properties": {"name": "City B", "type": "Major"},
            "geometry": {"type": "Point", "coordinates": [30, 20]}
        },
        {
            "type": "Feature",
            "properties": {"name": "City C", "type": "Minor"},
            "geometry": {"type": "Point", "coordinates": [-5, 35]}
        }
    ]
}


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


def map_component() -> rx.Component:
    """Create the MapLibre GL map component."""
    import json
    regions_json = json.dumps(regions_data)
    points_json = json.dumps(points_data)
    
    map_script = f"""
        const regionsData = {regions_json};
        const pointsData = {points_json};
        
        function initMap() {{
            if (window.map) return;
            
            if (typeof maplibregl === 'undefined') {{
                console.log('MapLibre GL not loaded yet, retrying...');
                setTimeout(initMap, 100);
                return;
            }}
            
            console.log('Initializing map...');
            
            try {{
                window.map = new maplibregl.Map({{
                    container: 'map',
                    style: 'https://demotiles.maplibre.org/style.json',
                    center: [15, 35],
                    zoom: 3
                }});
                
                console.log('Map created successfully');
                
                window.map.addControl(new maplibregl.NavigationControl(), 'top-right');
                
                window.map.on('load', () => {{
                    console.log('Map loaded');
                    window.map.addSource('regions', {{
                        type: 'geojson',
                        data: regionsData
                    }});
                    
                    window.map.addLayer({{
                        id: 'regions-fill',
                        type: 'fill',
                        source: 'regions',
                        paint: {{
                            'fill-color': '#088',
                            'fill-opacity': 0.4
                        }}
                    }});
                    
                    window.map.addLayer({{
                        id: 'regions-outline',
                        type: 'line',
                        source: 'regions',
                        paint: {{
                            'line-color': '#088',
                            'line-width': 2
                        }}
                    }});
                    
                    window.map.addSource('points', {{
                        type: 'geojson',
                        data: pointsData
                    }});
                    
                    window.map.addLayer({{
                        id: 'points',
                        type: 'circle',
                        source: 'points',
                        paint: {{
                            'circle-radius': 8,
                            'circle-color': '#f30',
                            'circle-stroke-width': 2,
                            'circle-stroke-color': '#fff'
                        }}
                    }});
                    
                    window.map.on('click', 'regions-fill', (e) => {{
                        const props = e.features[0].properties;
                        new maplibregl.Popup()
                            .setLngLat(e.lngLat)
                            .setHTML('<strong>' + props.name + '</strong><br>Population: ' + props.population.toLocaleString())
                            .addTo(window.map);
                    }});
                    
                    window.map.on('click', 'points', (e) => {{
                        const props = e.features[0].properties;
                        new maplibregl.Popup()
                            .setLngLat(e.lngLat)
                            .setHTML('<strong>' + props.name + '</strong><br>Type: ' + props.type)
                            .addTo(window.map);
                    }});
                    
                    window.map.on('mouseenter', 'regions-fill', () => {{
                        window.map.getCanvas().style.cursor = 'pointer';
                    }});
                    
                    window.map.on('mouseleave', 'regions-fill', () => {{
                        window.map.getCanvas().style.cursor = '';
                    }});
                    
                    window.map.on('mouseenter', 'points', () => {{
                        window.map.getCanvas().style.cursor = 'pointer';
                    }});
                    
                    window.map.on('mouseleave', 'points', () => {{
                        window.map.getCanvas().style.cursor = '';
                    }});
                }});
                
                window.map.on('error', (e) => {{
                    console.error('Map error:', e);
                }});
            }} catch (error) {{
                console.error('Error initializing map:', error);
            }}
        }}
        
        setTimeout(initMap, 500);
    """
    
    return rx.box(
        rx.el.link(
            href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css",
            rel="stylesheet"
        ),
        rx.script(src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"),
        rx.box(
            id="map",
            width="100%",
            height="calc(100vh - 80px)",
            background_color="lightgray",
        ),
        rx.script(map_script),
        width="100%",
        height="calc(100vh - 80px)",
    )


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


def index() -> rx.Component:
    """The main page."""
    import json
    regions_json = json.dumps(regions_data)
    points_json = json.dumps(points_data)
    
    return rx.fragment(
        rx.script(src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"),
        rx.html(
            f'<link href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css" rel="stylesheet" />'
        ),
        rx.box(
            rx.heading(
                "Reflex Data App with Interactive Map",
                size="7",
                text_align="center",
                padding="20px",
                background="white",
                z_index="999",
                position="relative",
            ),
            layer_controls(),
            position="relative",
            z_index="1000",
        ),
        rx.box(
            id="map",
            width="100%",
            height="calc(100vh - 80px)",
            background_color="lightgray",
        ),
        rx.html(f"""
            <script>
                console.log('TEST: Script is executing!');
                console.log('TEST: maplibregl type:', typeof maplibregl);
                
                const regionsData = {regions_json};
                const pointsData = {points_json};
                
                function initMap() {{
                    console.log('TEST: initMap called');
                    
                    if (window.map) {{
                        console.log('TEST: Map already exists');
                        return;
                    }}
                    
                    if (typeof maplibregl === 'undefined') {{
                        console.log('TEST: MapLibre not loaded, retrying in 100ms');
                        setTimeout(initMap, 100);
                        return;
                    }}
                    
                    console.log('TEST: Creating map...');
                    
                    const mapEl = document.getElementById('map');
                    if (!mapEl) {{
                        console.error('TEST: Map element not found!');
                        setTimeout(initMap, 100);
                        return;
                    }}
                    
                    console.log('TEST: Map element found:', mapEl);
                    
                    try {{
                        window.map = new maplibregl.Map({{
                            container: 'map',
                            style: 'https://demotiles.maplibre.org/style.json',
                            center: [15, 35],
                            zoom: 3
                        }});
                        
                        console.log('TEST: Map object created');
                        
                        window.map.on('load', () => {{
                            console.log('TEST: Map loaded successfully!');
                        }});
                        
                        window.map.on('error', (e) => {{
                            console.error('TEST: Map error:', e);
                        }});
                    }} catch (error) {{
                        console.error('TEST: Error creating map:', error);
                    }}
                }}
                
                console.log('TEST: Setting timeout for initMap');
                setTimeout(initMap, 1000);
            </script>
        """),
        rx.el.style("""
            body {
                margin: 0;
                padding: 0;
            }
        """),
    )


app = rx.App()
app.add_page(index)
