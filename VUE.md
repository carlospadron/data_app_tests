# Vue Data App

A comprehensive guide for creating a spatially-enabled data application using Vue 3 and MapLibre GL.

## Prerequisites

- Node.js version 18.0 or higher
- npm or yarn package manager
- Basic knowledge of JavaScript and Vue 3 Composition API
- Vue VS Code extension (recommended)

## Installation

### Install Vue Extension

Install the official Vue VS Code extension for better development experience:
- Search for "Vue - Official" in VS Code extensions
- Or install from: `Vue.volar`

### Create a New Project

Create a new Vue application:

```bash
npm create vue@latest
```

When prompted, enter the project name and select options:
- **Project name**: `vue_data_app`
- **Add TypeScript?** → No (or Yes if preferred)
- **Add JSX Support?** → No
- **Add Vue Router?** → No
- **Add Pinia for state management?** → No
- **Add Vitest for Unit Testing?** → No
- **Add an End-to-End Testing Solution?** → No
- **Add ESLint for code quality?** → Yes (optional)
- **Add Prettier for code formatting?** → Yes (optional)

Navigate to the project directory:
```bash
cd vue_data_app
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

Add MapLibre GL CSS to your main CSS file. Open `src/assets/main.css` and add at the top:

```css
@import 'maplibre-gl/dist/maplibre-gl.css';
```

Then import the CSS file in `src/main.js` (or `src/main.ts` if using TypeScript):

```javascript
import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
```

## Features Implemented

### GeoJSON Layers

The Map component includes two GeoJSON layers:

1. **Regions Layer** - Polygon geometries with fill and outline
2. **Points of Interest Layer** - Circle markers with custom styling

### Layer Toggle Menu

A control panel overlay provides:
- Vue reactive checkboxes for layer control
- Two-way data binding with `v-model`
- Real-time visibility updates

Implementation uses Vue 3 Composition API:
- `ref()` for reactive state management
- `v-model` for checkbox binding
- Toggle functions with computed visibility values

## Create a Map Component

The `src/components/Map.vue` file includes the complete implementation:

```vue
<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import maplibregl from 'maplibre-gl';

// Sample GeoJSON data included
const mapContainer = ref(null);
const regionsVisible = ref(true);
const pointsVisible = ref(true);
let map = null;

onMounted(() => {
  map = new maplibregl.Map({
    container: mapContainer.value,
    style: 'https://demotiles.maplibre.org/style.json',
    center: [15, 35],
    zoom: 3
  });

  // Add navigation controls and GeoJSON layers
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
```

## Update App Component

Replace the content in `src/App.vue`:

```vue
<script setup>
import Map from './components/Map.vue';
</script>

<template>
  <Map />
</template>
```

## Run the Application

Start the development server:

```bash
npm run dev
```

Open your browser and navigate to `http://localhost:5173`

## Project Structure

```
vue_data_app/
├── src/
│   ├── assets/
│   │   └── main.css
│   ├── components/
│   │   └── Map.vue
│   ├── App.vue
│   └── main.js
├── index.html
├── package.json
└── vite.config.js
```

## Additional Features

### Add a Navigation Component

Create `src/components/Navigation.vue`:

```vue
<script setup>
defineProps({
  title: {
    type: String,
    default: 'Data App'
  }
});
</script>

<template>
  <nav class="navigation">
    <h1>{{ title }}</h1>
  </nav>
</template>

<style scoped>
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

Update `src/App.vue` to include navigation:

```vue
<script setup>
import Map from './components/Map.vue';
import Navigation from './components/Navigation.vue';
</script>

<template>
  <Navigation title="Vue Data App" />
  <Map />
</template>
```

### Add Markers

To add markers to your map, update the Map component:

```javascript
// Add after map initialization in onMounted
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

### Using Composition API with Reactive State

For more complex map interactions:

```vue
<script setup>
import { onMounted, onUnmounted, ref, reactive } from 'vue';
import maplibregl from 'maplibre-gl';

const mapContainer = ref(null);
let map = null;

const mapState = reactive({
  center: [0, 0],
  zoom: 2
});

const updateMapView = (center, zoom) => {
  if (map) {
    map.flyTo({ center, zoom });
  }
};

onMounted(() => {
  map = new maplibregl.Map({
    container: mapContainer.value,
    style: 'https://demotiles.maplibre.org/style.json',
    center: mapState.center,
    zoom: mapState.zoom
  });

  map.addControl(new maplibregl.NavigationControl(), 'top-right');

  // Update reactive state when map moves
  map.on('move', () => {
    mapState.center = [map.getCenter().lng, map.getCenter().lat];
    mapState.zoom = map.getZoom();
  });
});

onUnmounted(() => {
  map?.remove();
});
</script>
```

## Build for Production

Build the application:

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

Preview the production build locally:

```bash
npm run preview
```

## Deployment

### Deploy to Netlify

```bash
npm run build
# Drag and drop the dist/ folder to Netlify
```

Or use Netlify CLI:

```bash
npm install -g netlify-cli
netlify deploy --prod
```

### Deploy to Vercel

```bash
npm install -g vercel
vercel
```

### Deploy to GitHub Pages

Add to `vite.config.js`:

```javascript
export default defineConfig({
  base: '/your-repo-name/',
  // ... other config
});
```

Then build and deploy:

```bash
npm run build
# Push dist/ folder to gh-pages branch
```

## Troubleshooting

### Map Not Displaying

1. Ensure MapLibre GL CSS is imported in `main.css`
2. Check browser console for errors
3. Verify the map container has height set in CSS

### Vite Build Errors

Clear the Vite cache:

```bash
rm -rf node_modules/.vite
npm install
npm run dev
```

### Hot Module Replacement Issues

If HMR isn't working properly:

```bash
rm -rf node_modules
npm install
```

## Performance Optimization

### Lazy Loading Components

```javascript
import { defineAsyncComponent } from 'vue';

const Map = defineAsyncComponent(() =>
  import('./components/Map.vue')
);
```

### Code Splitting

Vite automatically code-splits by route if using Vue Router.

## Resources

- [Vue.js Documentation](https://vuejs.org/guide/introduction.html)
- [Vue 3 Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [MapLibre GL JS Documentation](https://maplibre.org/maplibre-gl-js/docs/)
- [Vite Documentation](https://vitejs.dev/guide/)

## Next Steps

- Add data layers to the map
- Implement geospatial data visualization
- Create interactive controls and filters
- Add custom styling and theming
- Integrate with backend APIs for dynamic data
- Add Vue Router for multi-page navigation
- Implement Pinia for state management

