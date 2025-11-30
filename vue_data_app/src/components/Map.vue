<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import maplibregl from 'maplibre-gl';

const mapContainer = ref(null);
let map = null;

onMounted(() => {
  map = new maplibregl.Map({
    container: mapContainer.value,
    style: 'https://demotiles.maplibre.org/style.json',
    center: [0, 0],
    zoom: 2
  });

  // Add navigation controls
  map.addControl(new maplibregl.NavigationControl(), 'top-right');
});

onUnmounted(() => {
  map?.remove();
});
</script>

<template>
  <div ref="mapContainer" class="map-container"></div>
</template>

<style scoped>
.map-container {
  width: 100%;
  height: 100vh;
}
</style>
