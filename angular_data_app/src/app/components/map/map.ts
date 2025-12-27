import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import * as maplibregl from 'maplibre-gl';

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

@Component({
  selector: 'app-map',
  imports: [CommonModule],
  templateUrl: './map.html',
  styleUrl: './map.css',
})
export class Map implements OnInit, OnDestroy {
  map: maplibregl.Map | undefined;
  regionsVisible = true;
  pointsVisible = true;

  ngOnInit(): void {
    this.map = new maplibregl.Map({
      container: 'map',
      style: 'https://demotiles.maplibre.org/style.json',
      center: [15, 35],
      zoom: 3
    });

    // Add navigation controls
    this.map.addControl(new maplibregl.NavigationControl(), 'top-right');

    // Add GeoJSON layers when map loads
    this.map.on('load', () => {
      this.addGeoJSONLayers();
    });
  }

  addGeoJSONLayers(): void {
    if (!this.map) return;

    // Add regions layer
    this.map.addSource('regions', {
      type: 'geojson',
      data: regionsData as any
    });

    this.map.addLayer({
      id: 'regions-fill',
      type: 'fill',
      source: 'regions',
      paint: {
        'fill-color': '#088',
        'fill-opacity': 0.4
      }
    });

    this.map.addLayer({
      id: 'regions-outline',
      type: 'line',
      source: 'regions',
      paint: {
        'line-color': '#088',
        'line-width': 2
      }
    });

    // Add points layer
    this.map.addSource('points', {
      type: 'geojson',
      data: pointsData as any
    });

    this.map.addLayer({
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
  }

  toggleRegions(): void {
    if (!this.map) return;
    this.regionsVisible = !this.regionsVisible;
    const visibility = this.regionsVisible ? 'visible' : 'none';
    this.map.setLayoutProperty('regions-fill', 'visibility', visibility);
    this.map.setLayoutProperty('regions-outline', 'visibility', visibility);
  }

  togglePoints(): void {
    if (!this.map) return;
    this.pointsVisible = !this.pointsVisible;
    const visibility = this.pointsVisible ? 'visible' : 'none';
    this.map.setLayoutProperty('points', 'visibility', visibility);
  }

  ngOnDestroy(): void {
    this.map?.remove();
  }
}
