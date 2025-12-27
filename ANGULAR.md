# Angular Data App

A comprehensive guide for creating a spatially-enabled data application using Angular and MapLibre GL.

## Prerequisites

- Node.js version ^20.19.0 || ^22.12.0 || >=24.0.0
- Angular CLI installed globally
- Basic knowledge of TypeScript and Angular

## Installation

### Install Angular CLI

```bash
npm install -g @angular/cli
```

Verify installation:
```bash
ng version
```

## Create a New Project

Create a new Angular application:

```bash
ng new angular_data_app
```

When prompted:
- **Would you like to add Angular routing?** → Yes
- **Which stylesheet format would you like to use?** → CSS (or your preference)

Navigate to the project directory:
```bash
cd angular_data_app
```

## Install MapLibre GL

Install MapLibre GL and its TypeScript types:

```bash
npm install maplibre-gl
npm install --save-dev @types/maplibre-gl
```

## Configure Styles

Add MapLibre GL CSS to your `angular.json` file. Find the `styles` array and add the MapLibre CSS:

```json
"styles": [
  "src/styles.css",
  "node_modules/maplibre-gl/dist/maplibre-gl.css"
]
```

## Create a Map Component

Generate a new component for the map:

```bash
ng generate component components/map
```

## Implement the Map Component

### Update `map.component.ts`

```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';
import * as maplibregl from 'maplibre-gl';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit, OnDestroy {
  map: maplibregl.Map | undefined;

  ngOnInit(): void {
    this.map = new maplibregl.Map({
      container: 'map',
      style: 'https://demotiles.maplibre.org/style.json',
      center: [0, 0],
      zoom: 2
    });

    // Add navigation controls
    this.map.addControl(new maplibregl.NavigationControl(), 'top-right');
  }

  ngOnDestroy(): void {
    this.map?.remove();
  }
}
```

### Update `map.component.html`

```html
<div id="map"></div>
```

### Update `map.component.css`

```css
#map {
  width: 100%;
  height: 100vh;
}
```

## Update App Component

Replace the content in `app.component.html` with:

```html
<app-map></app-map>
```

## Run the Application

Start the development server:

```bash
ng serve
```

Open your browser and navigate to `http://localhost:4200`

## Project Structure

```
angular_data_app/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   └── map/
│   │   │       ├── map.component.ts
│   │   │       ├── map.component.html
│   │   │       └── map.component.css
│   │   ├── app.component.ts
│   │   ├── app.component.html
│   │   └── app.module.ts
│   └── styles.css
├── angular.json
└── package.json
```

## Features Implemented

### GeoJSON Layers

The application includes two GeoJSON layers:

1. **Regions Layer** - Displays polygon regions with properties like name and population
2. **Points of Interest Layer** - Shows point markers for cities and landmarks

### Layer Toggle Menu

A control panel in the top-left corner allows users to:
- Toggle each layer on/off independently
- See which layers are currently visible
- Control layer visibility in real-time

The implementation uses Angular's reactive state management with `regionsVisible` and `pointsVisible` properties to control layer visibility.

## Additional Features

### Add a Map Service

Create a service to manage map-related functionality:

```bash
ng generate service services/map
```

### Add More Markers

To add additional markers to your map, update `map.component.ts`:

```typescript
// Add after map initialization
new maplibregl.Marker()
  .setLngLat([0, 0])
  .addTo(this.map);
```

### Add Popup

```typescript
const popup = new maplibregl.Popup({ offset: 25 })
  .setText('Hello World!');

new maplibregl.Marker()
  .setLngLat([0, 0])
  .setPopup(popup)
  .addTo(this.map);
```

## Build for Production

Build the application:

```bash
ng build
```

The build artifacts will be stored in the `dist/` directory.

## Troubleshooting

### Map Not Displaying

1. Ensure MapLibre GL CSS is imported in `angular.json`
2. Check browser console for errors
3. Verify map container has height set in CSS

### TypeScript Errors

If you encounter TypeScript errors with MapLibre GL types:

```bash
npm install --save-dev @types/maplibre-gl
```

### Build Errors

Clear the Angular cache:

```bash
ng cache clean
npm install
```

## Resources

- [Angular Documentation](https://angular.dev)
- [MapLibre GL JS Documentation](https://maplibre.org/maplibre-gl-js/docs/)
- [Angular CLI Documentation](https://angular.dev/cli)

## Next Steps

- Add data layers to the map
- Implement geospatial data visualization
- Create interactive controls and filters
- Add custom styling and theming
- Integrate with backend APIs for dynamic data