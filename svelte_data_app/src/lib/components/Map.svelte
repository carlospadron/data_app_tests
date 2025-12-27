<script>
	import { onMount, onDestroy } from 'svelte';
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

	let mapContainer;
	let map;
	let mapLoaded = false;
	let regionsVisible = true;
	let pointsVisible = true;

	onMount(() => {
		map = new maplibregl.Map({
			container: mapContainer,
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
					'circle-radius': 8,
					'circle-color': '#f30',
					'circle-stroke-color': '#fff',
					'circle-stroke-width': 2
				}
			});
		});
	});

	onDestroy(() => {
		if (map) {
			map.remove();
		}
	});

	function toggleRegions() {
		if (!map || !mapLoaded) return;
		const visibility = regionsVisible ? 'visible' : 'none';
		map.setLayoutProperty('regions-fill', 'visibility', visibility);
		map.setLayoutProperty('regions-outline', 'visibility', visibility);
	}

	function togglePoints() {
		if (!map || !mapLoaded) return;
		const visibility = pointsVisible ? 'visible' : 'none';
		map.setLayoutProperty('points', 'visibility', visibility);
	}
</script>

<div bind:this={mapContainer} class="map-container"></div>

<div class="layer-control">
	<h3>Layers</h3>
	<div class="layer-item">
		<label>
			<input type="checkbox" bind:checked={regionsVisible} on:change={toggleRegions} />
			Regions
		</label>
	</div>
	<div class="layer-item">
		<label>
			<input type="checkbox" bind:checked={pointsVisible} on:change={togglePoints} />
			Points of Interest
		</label>
	</div>
</div>

<style>
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

	.layer-item input[type='checkbox'] {
		margin-right: 8px;
		cursor: pointer;
	}
</style>
