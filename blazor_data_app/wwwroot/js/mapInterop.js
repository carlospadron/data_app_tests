// MapLibre GL JS interop for Blazor WebAssembly
let map = null;
let mapLoaded = false;
let selectedPointId = null;
let dotNetRef = null;

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
            id: 0,
            properties: { id: 0, name: 'City A', type: 'Capital' },
            geometry: { type: 'Point', coordinates: [0, 40] }
        },
        {
            type: 'Feature',
            id: 1,
            properties: { id: 1, name: 'City B', type: 'Major' },
            geometry: { type: 'Point', coordinates: [30, 20] }
        },
        {
            type: 'Feature',
            id: 2,
            properties: { id: 2, name: 'City C', type: 'Minor' },
            geometry: { type: 'Point', coordinates: [-5, 35] }
        }
    ]
};

export function initializeMap(containerId, dotNetObject) {
    dotNetRef = dotNetObject;
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
                'circle-radius': ['case', ['boolean', ['feature-state', 'selected'], false], 14, 10],
                'circle-color': ['case', ['boolean', ['feature-state', 'selected'], false], '#facc15', '#f30'],
                'circle-stroke-color': '#fff',
                'circle-stroke-width': ['case', ['boolean', ['feature-state', 'selected'], false], 3, 2]
            }
        });

        map.on('click', async (event) => {
            const tolerancePx = 24;
            const maxDistSq = tolerancePx * tolerancePx;
            let nearestId = null;
            let nearestDistSq = Number.POSITIVE_INFINITY;

            for (const feature of pointsData.features) {
                const [lon, lat] = feature.geometry.coordinates;
                const projected = map.project([lon, lat]);
                const dx = projected.x - event.point.x;
                const dy = projected.y - event.point.y;
                const distSq = dx * dx + dy * dy;

                if (distSq < nearestDistSq) {
                    nearestDistSq = distSq;
                    nearestId = Number(feature.properties.id);
                }
            }

            if (nearestId === null || nearestDistSq > maxDistSq) return;

            focusPoint(nearestId);
            if (dotNetRef) {
                await dotNetRef.invokeMethodAsync('OnPointSelectedFromMap', nearestId);
            }
        });

        map.on('mouseenter', 'points', () => {
            map.getCanvas().style.cursor = 'pointer';
        });

        map.on('mouseleave', 'points', () => {
            map.getCanvas().style.cursor = '';
        });
    });
}

function syncSelectedPoint(pointId) {
    if (!map || !mapLoaded) return;
    if (selectedPointId !== null) {
        map.setFeatureState({ source: 'points', id: selectedPointId }, { selected: false });
    }
    if (pointId !== null) {
        map.setFeatureState({ source: 'points', id: pointId }, { selected: true });
    }
    selectedPointId = pointId;
}

export function focusPoint(pointId) {
    if (!map || !mapLoaded) return;
    const feature = pointsData.features.find((item) => item.properties.id === pointId);
    if (!feature) return;
    map.flyTo({ center: feature.geometry.coordinates, zoom: 5, essential: true });
    syncSelectedPoint(pointId);
}

export function getPoints() {
    return pointsData.features.map((feature) => ({
        id: feature.properties.id,
        name: feature.properties.name,
        type: feature.properties.type,
        lon: feature.geometry.coordinates[0],
        lat: feature.geometry.coordinates[1]
    }));
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
        selectedPointId = null;
        dotNetRef = null;
    }
}
