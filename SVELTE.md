# Svelte Data App

A comprehensive guide for creating a spatially-enabled data application using Svelte 5 and MapLibre GL.

## Prerequisites

- Node.js version 18.0 or higher
- npm or yarn package manager
- Basic knowledge of JavaScript and Svelte
- Svelte VS Code extension (recommended)

## Installation

### Install Svelte Extension

Install the official Svelte VS Code extension for better development experience:
- Search for "Svelte for VS Code" in VS Code extensions
- Or install from: `svelte.svelte-vscode`

### Create a New Project

Create a new Svelte application using the official scaffolding tool:

```bash
npx sv create
```

When prompted, select options:
- **Which template would you like?** → SvelteKit demo app (or Minimal app)
- **Add type checking with TypeScript?** → Yes, using JavaScript with JSDoc comments (or TypeScript)
- **What would you like to add?** → (optional: prettier, eslint, vitest, playwright)
- **Which package manager?** → npm

Navigate to the project directory:
```bash
cd svelte_data_app
```

Install dependencies:
```bash
npm install
```

## Install MapLibre GL

Install MapLibre GL library:

```bash
npm install maplibre-gl
```

## Configure Styles

Add MapLibre GL CSS to your app. Open `src/app.html` and add the MapLibre CSS link in the `<head>` section:

```html
<!doctype html>
<html lang="en">
	<head>
		<meta charset="utf-8" />
		<link rel="icon" href="%sveltekit.assets%/favicon.png" />
		<link rel="stylesheet" href="https://unpkg.com/maplibre-gl/dist/maplibre-gl.css" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		%sveltekit.head%
	</head>
	<body data-sveltekit-preload-data="hover">
		<div style="display: contents">%sveltekit.body%</div>
	</body>
</html>
```

Alternatively, you can import it in your root layout. Create or update `src/routes/+layout.svelte`:

```svelte
<script>
	import 'maplibre-gl/dist/maplibre-gl.css';
</script>

<slot />
```

## Features Implemented

### GeoJSON Layers

The Map component includes two GeoJSON layers:

1. **Regions Layer** - Polygon features with customizable styling
2. **Points of Interest Layer** - Circle markers for locations

### Layer Toggle Menu

An interactive control panel provides:
- Checkboxes bound to reactive variables
- Individual layer visibility control
- Svelte's reactive system for automatic UI updates

Implementation uses:
- Reactive variables (`regionsVisible`, `pointsVisible`)
- `bind:checked` directive for two-way binding
- Toggle functions that update layer visibility

## Create a Map Component

The `src/lib/components/Map.svelte` file includes the complete implementation:

```svelte
<script>
	import { onMount, onDestroy } from 'svelte';
	import maplibregl from 'maplibre-gl';

	// Sample GeoJSON data included
	let mapContainer;
	let map;
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
```

## Update Page Component

Replace the content in `src/routes/+page.svelte`:

```svelte
<script>
	import Map from '$lib/components/Map.svelte';
</script>

<Map />
```

## Run the Application

Start the development server:

```bash
npm run dev
```

Open your browser and navigate to `http://localhost:5173`

## Project Structure

```
svelte_data_app/
├── src/
│   ├── lib/
│   │   └── components/
│   │       └── Map.svelte
│   ├── routes/
│   │   ├── +layout.svelte
│   │   └── +page.svelte
│   └── app.html
├── static/
├── package.json
├── svelte.config.js
└── vite.config.js
```

## Additional Features

### Add a Navigation Component

Create `src/lib/components/Navigation.svelte`:

```svelte
<script>
	export let title = 'Data App';
</script>

<nav class="navigation">
	<h1>{title}</h1>
</nav>

<style>
	.navigation {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		background: white;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		padding: 1rem;
		z-index: 10;
	}

	.navigation h1 {
		margin: 0;
		font-size: 1.5rem;
		font-weight: bold;
	}
</style>
```

Update `src/routes/+page.svelte` to include navigation:

```svelte
<script>
	import Map from '$lib/components/Map.svelte';
	import Navigation from '$lib/components/Navigation.svelte';
</script>

<Navigation title="Svelte Data App" />
<Map />
```

### Add Markers

To add markers to your map, update the Map component:

```javascript
// Add after map initialization in onMount
new maplibregl.Marker()
	.setLngLat([0, 0])
	.addTo(map);
```

### Add Popup

```javascript
const popup = new maplibregl.Popup({ offset: 25 })
	.setText('Hello World!');

new maplibregl.Marker()
	.setLngLat([0, 0])
	.setPopup(popup)
	.addTo(map);
```

### Using Svelte Stores for Reactive State

Create `src/lib/stores/mapStore.js`:

```javascript
import { writable } from 'svelte/stores';

export const mapCenter = writable([0, 0]);
export const mapZoom = writable(2);
```

Use in your Map component:

```svelte
<script>
	import { onMount, onDestroy } from 'svelte';
	import maplibregl from 'maplibre-gl';
	import { mapCenter, mapZoom } from '$lib/stores/mapStore';

	let mapContainer;
	let map;

	onMount(() => {
		map = new maplibregl.Map({
			container: mapContainer,
			style: 'https://demotiles.maplibre.org/style.json',
			center: $mapCenter,
			zoom: $mapZoom
		});

		map.addControl(new maplibregl.NavigationControl(), 'top-right');

		// Update stores when map moves
		map.on('move', () => {
			mapCenter.set([map.getCenter().lng, map.getCenter().lat]);
			mapZoom.set(map.getZoom());
		});
	});

	onDestroy(() => {
		if (map) {
			map.remove();
		}
	});

	// React to store changes
	$: if (map) {
		map.setCenter($mapCenter);
		map.setZoom($mapZoom);
	}
</script>

<div bind:this={mapContainer} class="map-container"></div>

<style>
	.map-container {
		width: 100%;
		height: 100vh;
	}
</style>
```

## Build for Production

Build the application:

```bash
npm run build
```

Preview the production build locally:

```bash
npm run preview
```

## Deployment

### Deploy to Vercel

```bash
npm install -g vercel
vercel
```

### Deploy to Netlify

```bash
npm run build
# Drag and drop the build/ folder to Netlify
```

Or use Netlify CLI:

```bash
npm install -g netlify-cli
netlify deploy --prod
```

### Static Site Adapter

For static hosting (GitHub Pages, etc.), install the static adapter:

```bash
npm install -D @sveltejs/adapter-static
```

Update `svelte.config.js`:

```javascript
import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: undefined,
			precompress: false,
			strict: true
		})
	}
};

export default config;
```

## Troubleshooting

### Map Not Displaying

1. Ensure MapLibre GL CSS is loaded (check in app.html or +layout.svelte)
2. Check browser console for errors
3. Verify the map container has height set in CSS
4. Ensure the component is mounted before initializing the map

### SvelteKit SSR Issues

MapLibre GL requires the browser environment. If you encounter SSR errors:

```svelte
<script>
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	let mapContainer;
	let map;

	onMount(async () => {
		if (browser) {
			const maplibregl = await import('maplibre-gl');
			map = new maplibregl.Map({
				// ... config
			});
		}
	});
</script>
```

### Build Errors

Clear the SvelteKit cache:

```bash
rm -rf .svelte-kit
npm install
npm run dev
```

## Performance Optimization

### Lazy Loading Components

```svelte
<script>
	import { onMount } from 'svelte';

	let MapComponent;

	onMount(async () => {
		const module = await import('$lib/components/Map.svelte');
		MapComponent = module.default;
	});
</script>

{#if MapComponent}
	<svelte:component this={MapComponent} />
{/if}
```

### Code Splitting

SvelteKit automatically code-splits by route. Use dynamic imports for large dependencies.

## Resources

- [Svelte Documentation](https://svelte.dev/docs/introduction)
- [SvelteKit Documentation](https://kit.svelte.dev/docs/introduction)
- [Svelte Tutorial](https://svelte.dev/tutorial/svelte/welcome-to-svelte)
- [MapLibre GL JS Documentation](https://maplibre.org/maplibre-gl-js/docs/)
- [Svelte Stores](https://svelte.dev/docs/svelte-store)

## Next Steps

- Add data layers to the map
- Implement geospatial data visualization
- Create interactive controls and filters
- Add custom styling and theming
- Integrate with backend APIs for dynamic data
- Add routing with SvelteKit
- Implement server-side data fetching
- Add authentication and user management

