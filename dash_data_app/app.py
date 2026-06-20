import dash
from dash import dcc, html, Input, Output, State, callback, dash_table, ctx
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

points_data = [
    {"id": 0, "name": "City A", "type": "Capital", "lat": 40, "lon": 0},
    {"id": 1, "name": "City B", "type": "Major", "lat": 20, "lon": 30},
    {"id": 2, "name": "City C", "type": "Minor", "lat": 35, "lon": -5}
]

# Layout
app.layout = html.Div([
    html.H1("Dash Data App with Interactive Map", style={
        'textAlign': 'center',
        'marginBottom': '20px',
        'marginTop': '20px'
    }),
    
    html.Div([
        html.Div([
            html.H3("Layers", style={'marginBottom': '10px'}),
            
            dcc.Checklist(
                id='layer-toggles',
                options=[
                    {'label': ' Regions', 'value': 'regions'},
                    {'label': ' Points of Interest', 'value': 'points'}
                ],
                value=['regions', 'points'],
                style={'fontSize': '14px'}
            )
        ], style={
            'position': 'absolute',
            'top': '80px',
            'left': '20px',
            'backgroundColor': 'white',
            'padding': '15px',
            'borderRadius': '4px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.3)',
            'zIndex': '1000',
            'minWidth': '200px'
        })
    ]),
    
    dcc.Graph(
        id='map',
        style={'height': '85vh'},
        config={'displayModeBar': True, 'scrollZoom': True, 'displaylogo': False}
    ),

    html.Div([
        html.H3('Points Table', style={'marginBottom': '8px'}),
        dash_table.DataTable(
            id='points-table',
            columns=[
                {'name': 'Name', 'id': 'name'},
                {'name': 'Type', 'id': 'type'},
                {'name': 'Coordinates', 'id': 'coords'}
            ],
            data=[
                {
                    'id': point['id'],
                    'name': point['name'],
                    'type': point['type'],
                    'coords': f"{point['lat']:.1f}, {point['lon']:.1f}"
                }
                for point in points_data
            ],
            row_selectable='single',
            selected_rows=[],
            style_cell={'padding': '6px', 'textAlign': 'left', 'fontSize': '13px'},
            style_header={'fontWeight': 'bold'},
            style_data_conditional=[
                {
                    'if': {'state': 'selected'},
                    'backgroundColor': '#fef3c7',
                    'border': '1px solid #e5e7eb'
                }
            ]
        )
    ], style={
        'position': 'absolute',
        'right': '20px',
        'bottom': '20px',
        'backgroundColor': 'white',
        'padding': '12px',
        'borderRadius': '4px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.3)',
        'zIndex': '1000',
        'minWidth': '320px'
    }),
    
    # Store to keep track of map state
    dcc.Store(id='map-state', data={'center': {'lat': 35, 'lon': 15}, 'zoom': 3}),
    dcc.Store(id='selected-point', data=None)
])

@callback(
    Output('map', 'figure'),
    Output('map-state', 'data'),
    Output('points-table', 'selected_rows'),
    Output('selected-point', 'data'),
    Input('layer-toggles', 'value'),
    Input('map', 'relayoutData'),
    Input('map', 'clickData'),
    Input('points-table', 'selected_rows'),
    State('map-state', 'data'),
    State('selected-point', 'data')
)
def update_map(selected_layers, relayout_data, click_data, selected_rows, map_state, selected_point):
    triggered_props = set(ctx.triggered_prop_ids.keys())

    # Update map viewport only when relayout triggered this callback.
    if 'map.relayoutData' in triggered_props and relayout_data and 'map.center' in relayout_data:
        map_state = {
            'center': relayout_data['map.center'],
            'zoom': relayout_data.get('map.zoom', map_state.get('zoom', 3)),
            'bearing': relayout_data.get('map.bearing', 0),
            'pitch': relayout_data.get('map.pitch', 0)
        }

    # Respect the actual trigger so stale clickData does not override table selection.
    if 'points-table.selected_rows' in triggered_props:
        if selected_rows and len(selected_rows) > 0:
            selected_point = points_data[selected_rows[0]]['id']
        else:
            selected_point = None
    elif 'map.clickData' in triggered_props and click_data and click_data.get('points'):
        point_custom = click_data['points'][0].get('customdata')
        if point_custom is not None:
            selected_point = int(point_custom[0])

    # Keep table selection in sync with selected point id.
    if selected_point is not None:
        selected_rows = [next((idx for idx, p in enumerate(points_data) if p['id'] == selected_point), 0)]
        selected_item = next((p for p in points_data if p['id'] == selected_point), None)
        if selected_item:
            map_state['center'] = {'lat': selected_item['lat'], 'lon': selected_item['lon']}
            map_state['zoom'] = max(map_state.get('zoom', 3), 5)
    else:
        selected_rows = []

    # Use stored state or defaults
    center = map_state.get('center', {'lat': 35, 'lon': 15})
    zoom = map_state.get('zoom', 3)
    bearing = map_state.get('bearing', 0)
    pitch = map_state.get('pitch', 0)

    fig = go.Figure()
    
    # Add regions layer if selected
    if 'regions' in selected_layers:
        for feature in regions_data['features']:
            coords = feature['geometry']['coordinates'][0]
            lons = [c[0] for c in coords]
            lats = [c[1] for c in coords]
            
            fig.add_trace(go.Scattermap(
                mode='lines',
                lon=lons,
                lat=lats,
                fill='toself',
                fillcolor='rgba(0, 136, 136, 0.4)',
                line=dict(color='rgb(0, 136, 136)', width=2),
                name=feature['properties']['name'],
                hovertemplate=f"<b>{feature['properties']['name']}</b><br>" +
                             f"Population: {feature['properties']['population']:,}<extra></extra>"
            ))
    
    # Add points layer if selected
    if 'points' in selected_layers:
        lons = [p['lon'] for p in points_data]
        lats = [p['lat'] for p in points_data]
        names = [p['name'] for p in points_data]
        types = [p['type'] for p in points_data]
        ids = [p['id'] for p in points_data]
        custom_data = [[item_id, item_type] for item_id, item_type in zip(ids, types)]
        marker_colors = ['#facc15' if p['id'] == selected_point else 'rgb(255, 51, 0)' for p in points_data]
        marker_sizes = [18 if p['id'] == selected_point else 14 for p in points_data]
        
        fig.add_trace(go.Scattermap(
            mode='markers',
            lon=lons,
            lat=lats,
            marker=dict(
                size=marker_sizes,
                color=marker_colors,
                opacity=1
            ),
            text=names,
            name='Points of Interest',
            hovertemplate="<b>%{text}</b><br>" +
                         "Type: %{customdata[1]}<extra></extra>",
            customdata=custom_data
        ))
    
    # Update layout with map style, preserving viewport state
    fig.update_layout(
        map=dict(
            style='https://demotiles.maplibre.org/style.json',
            center=center,
            zoom=zoom,
            bearing=bearing,
            pitch=pitch
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(255, 255, 255, 0.8)"
        ),
        hovermode='closest',
        uirevision='constant'  # Prevents map from resetting on updates
    )
    
    return fig, map_state, selected_rows or [], selected_point

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
