<script>
	import { onMount, onDestroy } from 'svelte';
	import maplibregl from 'maplibre-gl';

	let mapContainer;
	let map;

	onMount(() => {
		map = new maplibregl.Map({
			container: mapContainer,
			style: 'https://demotiles.maplibre.org/style.json',
			center: [0, 0],
			zoom: 2
		});

		// Add navigation controls
		map.addControl(new maplibregl.NavigationControl(), 'top-right');
	});

	onDestroy(() => {
		if (map) {
			map.remove();
		}
	});
</script>

<div bind:this={mapContainer} class="map-container"></div>

<style>
	.map-container {
		width: 100%;
		height: 100vh;
	}
</style>
