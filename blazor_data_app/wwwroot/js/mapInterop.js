// MapLibre GL JS interop for Blazor WebAssembly
let map = null;
let mapLoaded = false;

const regionsData = {
    type: 'FeatureCollection',
    features: [
        {
            type: 'Feature',
            properties: { name: 'Region A', population: 50000 },
            geometry: {
                type: 'Polygon',
                coordinates: [[
                    [-10, 30], [10, 30], [10, 50], [-10, 50], [-10, 30]
                ]]
            }
        },
        {
            type: 'Feature',
            properties: { name: 'Region B', population: 75000 },
            geometry: {
                type: 'Polygon',
                coordinates: [[
                    [20, 10], [40, 10], [40, 30], [20, 30], [20, 10]
                ]]
            }
        }
    ]
};

const pointsData = {
    type: 'FeatureCollection',
    features: [
        {
            type: 'Feature',
            properties: { name: 'City A', type: 'Capital' },
            geometry: { type: 'Point', coordinates: [0, 40] }
        },
        {
            type: 'Feature',
            properties: { name: 'City B', type: 'Major' },
            geometry: { type: 'Point', coordinates: [30, 20] }
        },
        {
            type: 'Feature',
            properties: { name: 'City C', type: 'Minor' },
            geometry: { type: 'Point', coordinates: [-5, 35] }
        }
    ]
};

export function initializeMap(containerId) {
    map = new maplibregl.Map({
        container: containerId,
        style: 'https://demotiles.maplibre.org/style.json',
        center: [15, 35],
        zoom: 3
    });

    map.addControl(new maplibregl.NavigationControl(), 'top-right');

    map.on('load', () => {
        mapLoaded = true;

        map.addSource('regions', {
            type: 'geojson',
            data: regionsData
        });

        map.addLayer({
            id: 'regions-fill',
            type: 'fill',
            source: 'regions',
            paint: {
                'fill-color': '#088',
                'fill-opacity': 0.4
            }
        });

        map.addLayer({
            id: 'regions-outline',
            type: 'line',
            source: 'regions',
            paint: {
                'line-color': '#088',
                'line-width': 2
            }
        });

        map.addSource('points', {
            type: 'geojson',
            data: pointsData
        });

        map.addLayer({
            id: 'points',
            type: 'circle',
            source: 'points',
            paint: {
                'circle-radius': 8,
                'circle-color': '#f30',
                'circle-stroke-color': '#fff',
                'circle-stroke-width': 2
            }
        });
    });
}

export function setLayerVisibility(layerIds, visible) {
    if (!map || !mapLoaded) return;
    const visibility = visible ? 'visible' : 'none';
    for (const layerId of layerIds) {
        map.setLayoutProperty(layerId, 'visibility', visibility);
    }
}

export function destroyMap() {
    if (map) {
        map.remove();
        map = null;
        mapLoaded = false;
    }
}
