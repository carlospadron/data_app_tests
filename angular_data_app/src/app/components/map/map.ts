import { Component, OnInit, OnDestroy, NgZone, signal } from '@angular/core';
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

@Component({
  selector: 'app-map',
  imports: [CommonModule],
  templateUrl: './map.html',
  styleUrl: './map.css',
})
export class Map implements OnInit, OnDestroy {
  constructor(private ngZone: NgZone) {}

  map: maplibregl.Map | undefined;
  regionsVisible = true;
  pointsVisible = true;
  selectedPointId = signal<number | null>(null);
  pointsTable = pointsData.features.map((feature) => ({
    id: feature.properties.id,
    name: feature.properties.name,
    type: feature.properties.type,
    lon: feature.geometry.coordinates[0],
    lat: feature.geometry.coordinates[1]
  }));

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
        'circle-radius': ['case', ['boolean', ['feature-state', 'selected'], false], 14, 10] as any,
        'circle-color': ['case', ['boolean', ['feature-state', 'selected'], false], '#facc15', '#f30'] as any,
        'circle-stroke-color': '#fff',
        'circle-stroke-width': ['case', ['boolean', ['feature-state', 'selected'], false], 3, 2] as any
      }
    });

    this.map.on('click', (event) => {
      if (!this.map) return;

      const tolerancePx = 24;
      const maxDistSq = tolerancePx * tolerancePx;
      let nearestId: number | null = null;
      let nearestDistSq = Number.POSITIVE_INFINITY;

      for (const point of this.pointsTable) {
        const projected = this.map.project([point.lon, point.lat]);
        const dx = projected.x - event.point.x;
        const dy = projected.y - event.point.y;
        const distSq = dx * dx + dy * dy;

        if (distSq < nearestDistSq) {
          nearestDistSq = distSq;
          nearestId = point.id;
        }
      }

      if (nearestId !== null && nearestDistSq <= maxDistSq) {
        this.ngZone.run(() => this.focusPoint(nearestId as number));
      }
    });

    this.map.on('mouseenter', 'points', () => {
      this.map?.getCanvas().style.setProperty('cursor', 'pointer');
    });

    this.map.on('mouseleave', 'points', () => {
      this.map?.getCanvas().style.setProperty('cursor', '');
    });
  }

  private syncSelectedPoint(nextId: number | null): void {
    if (!this.map || !this.map.getSource('points')) return;

    const prevId = this.selectedPointId();

    if (prevId !== null) {
      this.map.setFeatureState({ source: 'points', id: prevId }, { selected: false });
    }

    if (nextId !== null) {
      this.map.setFeatureState({ source: 'points', id: nextId }, { selected: true });
    }

    this.selectedPointId.set(nextId);
  }

  focusPoint(pointId: number): void {
    if (!this.map) return;
    const point = this.pointsTable.find((entry) => entry.id === pointId);
    if (!point) return;

    this.map.flyTo({ center: [point.lon, point.lat], zoom: 5, essential: true });
    this.syncSelectedPoint(pointId);
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
