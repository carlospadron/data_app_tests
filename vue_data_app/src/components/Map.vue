<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import maplibregl from 'maplibre-gl';

// Sample GeoJSON data
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

const pointsTable = pointsData.features.map((feature) => ({
  id: feature.properties.id,
  name: feature.properties.name,
  type: feature.properties.type,
  lon: feature.geometry.coordinates[0],
  lat: feature.geometry.coordinates[1]
}));

const mapContainer = ref(null);
const regionsVisible = ref(true);
const pointsVisible = ref(true);
const selectedPointId = ref(null);
let map = null;
let mapLoaded = false;

const syncSelectedPoint = (nextId) => {
  if (!map || !mapLoaded) return;
  if (selectedPointId.value !== null) {
    map.setFeatureState({ source: 'points', id: selectedPointId.value }, { selected: false });
  }
  if (nextId !== null) {
    map.setFeatureState({ source: 'points', id: nextId }, { selected: true });
  }
  selectedPointId.value = nextId;
};

const focusPoint = (pointId) => {
  const point = pointsTable.find((entry) => entry.id === pointId);
  if (!point || !map) return;
  map.flyTo({ center: [point.lon, point.lat], zoom: 5, essential: true });
  syncSelectedPoint(pointId);
};

onMounted(() => {
  map = new maplibregl.Map({
    container: mapContainer.value,
    style: 'https://demotiles.maplibre.org/style.json',
    center: [15, 35],
    zoom: 3
  });

  // Add navigation controls
  map.addControl(new maplibregl.NavigationControl(), 'top-right');

  // Add GeoJSON layers when map loads
  map.on('load', () => {
    mapLoaded = true;
    
    // Add regions source and layers
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

    // Add points source and layer
    map.addSource('points', {
      type: 'geojson',
      data: pointsData
    });

    map.addLayer({
      id: 'points',
      type: 'circle',
      source: 'points',
      paint: {
        'circle-radius': ['case', ['boolean', ['feature-state', 'selected'], false], 11, 8],
        'circle-color': ['case', ['boolean', ['feature-state', 'selected'], false], '#facc15', '#f30'],
        'circle-stroke-color': '#fff',
        'circle-stroke-width': ['case', ['boolean', ['feature-state', 'selected'], false], 3, 2]
      }
    });

    map.on('click', 'points', (event) => {
      const feature = event.features?.[0];
      if (!feature?.properties) return;
      const id = Number(feature.properties.id);
      if (!Number.isNaN(id)) {
        focusPoint(id);
      }
    });

    map.on('mouseenter', 'points', () => {
      map.getCanvas().style.cursor = 'pointer';
    });

    map.on('mouseleave', 'points', () => {
      map.getCanvas().style.cursor = '';
    });
  });
});

onUnmounted(() => {
  map?.remove();
});

const toggleRegions = () => {
  if (!map || !mapLoaded) return;
  const visibility = regionsVisible.value ? 'visible' : 'none';
  map.setLayoutProperty('regions-fill', 'visibility', visibility);
  map.setLayoutProperty('regions-outline', 'visibility', visibility);
};

const togglePoints = () => {
  if (!map || !mapLoaded) return;
  const visibility = pointsVisible.value ? 'visible' : 'none';
  map.setLayoutProperty('points', 'visibility', visibility);
};
</script>

<template>
  <div ref="mapContainer" class="map-container"></div>
  
  <div class="layer-control">
    <h3>Layers</h3>
    <div class="layer-item">
      <label>
        <input 
          type="checkbox" 
          v-model="regionsVisible" 
          @change="toggleRegions"
        />
        Regions
      </label>
    </div>
    <div class="layer-item">
      <label>
        <input 
          type="checkbox" 
          v-model="pointsVisible" 
          @change="togglePoints"
        />
        Points of Interest
      </label>
    </div>
  </div>

  <div class="table-control">
    <h3>Points Table</h3>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Type</th>
          <th>Coords</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="point in pointsTable"
          :key="point.id"
          :class="{ selected: selectedPointId === point.id }"
          @click="focusPoint(point.id)"
        >
          <td>{{ point.name }}</td>
          <td>{{ point.type }}</td>
          <td>{{ point.lat.toFixed(1) }}, {{ point.lon.toFixed(1) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.map-container {
  width: 100%;
  height: 100vh;
}

.layer-control {
  position: absolute;
  top: 10px;
  left: 10px;
  background: white;
  padding: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  z-index: 1;
  min-width: 200px;
}

.layer-control h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  font-weight: bold;
}

.layer-item {
  margin: 8px 0;
}

.layer-item label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 14px;
}

.layer-item input[type="checkbox"] {
  margin-right: 8px;
  cursor: pointer;
}

.table-control {
  position: absolute;
  right: 10px;
  bottom: 10px;
  background: white;
  padding: 12px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  z-index: 1;
  min-width: 320px;
}

.table-control h3 {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: bold;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

th,
td {
  text-align: left;
  padding: 6px;
  border-bottom: 1px solid #f0f0f0;
}

thead th {
  border-bottom: 1px solid #ddd;
}

tbody tr {
  cursor: pointer;
}

tbody tr.selected {
  background: #fef3c7;
}
</style>
