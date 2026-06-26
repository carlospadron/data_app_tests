'use client';

import { useEffect, useRef, useState } from 'react';
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

export default function Map() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const selectedPointIdRef = useRef<number | null>(null);
  const [regionsVisible, setRegionsVisible] = useState(true);
  const [pointsVisible, setPointsVisible] = useState(true);
  const [selectedPointId, setSelectedPointId] = useState<number | null>(null);

  const syncSelectedPoint = (nextId: number | null) => {
    if (!map.current || !map.current.getSource('points')) return;
    if (selectedPointIdRef.current !== null) {
      map.current.setFeatureState(
        { source: 'points', id: selectedPointIdRef.current },
        { selected: false }
      );
    }
    if (nextId !== null) {
      map.current.setFeatureState({ source: 'points', id: nextId }, { selected: true });
    }
    selectedPointIdRef.current = nextId;
    setSelectedPointId(nextId);
  };

  const focusPoint = (pointId: number) => {
    if (!map.current) return;
    const point = pointsTable.find((entry) => entry.id === pointId);
    if (!point) return;
    map.current.flyTo({ center: [point.lon, point.lat], zoom: 5, essential: true });
    syncSelectedPoint(pointId);
  };

  useEffect(() => {
    if (map.current) return; // Initialize map only once

    if (mapContainer.current) {
      map.current = new maplibregl.Map({
        container: mapContainer.current,
        style: 'https://demotiles.maplibre.org/style.json',
        center: [15, 35],
        zoom: 3
      });

      // Add navigation controls
      map.current.addControl(new maplibregl.NavigationControl(), 'top-right');

      // Add GeoJSON layers when map loads
      map.current.on('load', () => {
        if (!map.current) return;

        // Add regions source and layers
        map.current.addSource('regions', {
          type: 'geojson',
          data: regionsData as any
        });

        map.current.addLayer({
          id: 'regions-fill',
          type: 'fill',
          source: 'regions',
          paint: {
            'fill-color': '#088',
            'fill-opacity': 0.4
          }
        });

        map.current.addLayer({
          id: 'regions-outline',
          type: 'line',
          source: 'regions',
          paint: {
            'line-color': '#088',
            'line-width': 2
          }
        });

        // Add points source and layer
        map.current.addSource('points', {
          type: 'geojson',
          data: pointsData as any
        });

        map.current.addLayer({
          id: 'points',
          type: 'circle',
          source: 'points',
          paint: {
            'circle-radius': ['case', ['boolean', ['feature-state', 'selected'], false], 11, 8] as any,
            'circle-color': ['case', ['boolean', ['feature-state', 'selected'], false], '#facc15', '#f30'] as any,
            'circle-stroke-color': '#fff',
            'circle-stroke-width': ['case', ['boolean', ['feature-state', 'selected'], false], 3, 2] as any
          }
        });

        map.current.on('click', 'points', (event) => {
          const feature = event.features?.[0];
          if (!feature || !feature.properties) return;
          const id = Number((feature.properties as Record<string, unknown>).id);
          if (!Number.isNaN(id)) {
            focusPoint(id);
          }
        });

        map.current.on('mouseenter', 'points', () => {
          if (map.current) {
            map.current.getCanvas().style.cursor = 'pointer';
          }
        });

        map.current.on('mouseleave', 'points', () => {
          if (map.current) {
            map.current.getCanvas().style.cursor = '';
          }
        });
      });
    }

    return () => {
      map.current?.remove();
    };
  }, []);

  const toggleRegions = () => {
    if (!map.current) return;
    const newVisibility = !regionsVisible;
    setRegionsVisible(newVisibility);
    const visibility = newVisibility ? 'visible' : 'none';
    map.current.setLayoutProperty('regions-fill', 'visibility', visibility);
    map.current.setLayoutProperty('regions-outline', 'visibility', visibility);
  };

  const togglePoints = () => {
    if (!map.current) return;
    const newVisibility = !pointsVisible;
    setPointsVisible(newVisibility);
    const visibility = newVisibility ? 'visible' : 'none';
    map.current.setLayoutProperty('points', 'visibility', visibility);
  };

  return (
    <>
      <div 
        ref={mapContainer} 
        style={{ width: '100%', height: '100vh' }}
      />
      <div style={{
        position: 'absolute',
        top: '10px',
        left: '10px',
        background: 'white',
        padding: '15px',
        borderRadius: '4px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
        zIndex: 1,
        minWidth: '200px'
      }}>
        <h3 style={{ margin: '0 0 10px 0', fontSize: '16px', fontWeight: 'bold' }}>
          Layers
        </h3>
        <div style={{ margin: '8px 0' }}>
          <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
            <input
              type="checkbox"
              checked={regionsVisible}
              onChange={toggleRegions}
              style={{ marginRight: '8px', cursor: 'pointer' }}
            />
            Regions
          </label>
        </div>
        <div style={{ margin: '8px 0' }}>
          <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
            <input
              type="checkbox"
              checked={pointsVisible}
              onChange={togglePoints}
              style={{ marginRight: '8px', cursor: 'pointer' }}
            />
            Points of Interest
          </label>
        </div>
      </div>

      <div style={{
        position: 'absolute',
        right: '10px',
        bottom: '10px',
        background: 'white',
        padding: '12px',
        borderRadius: '4px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
        zIndex: 1,
        minWidth: '320px'
      }}>
        <h3 style={{ margin: '0 0 8px 0', fontSize: '16px', fontWeight: 'bold' }}>
          Points Table
        </h3>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px' }}>
          <thead>
            <tr>
              <th style={{ textAlign: 'left', borderBottom: '1px solid #ddd', padding: '6px' }}>Name</th>
              <th style={{ textAlign: 'left', borderBottom: '1px solid #ddd', padding: '6px' }}>Type</th>
              <th style={{ textAlign: 'left', borderBottom: '1px solid #ddd', padding: '6px' }}>Coords</th>
            </tr>
          </thead>
          <tbody>
            {pointsTable.map((point) => (
              <tr
                key={point.id}
                onClick={() => focusPoint(point.id)}
                style={{
                  cursor: 'pointer',
                  background: selectedPointId === point.id ? '#fef3c7' : 'transparent'
                }}
              >
                <td style={{ padding: '6px', borderBottom: '1px solid #f0f0f0' }}>{point.name}</td>
                <td style={{ padding: '6px', borderBottom: '1px solid #f0f0f0' }}>{point.type}</td>
                <td style={{ padding: '6px', borderBottom: '1px solid #f0f0f0' }}>
                  {point.lat.toFixed(1)}, {point.lon.toFixed(1)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
