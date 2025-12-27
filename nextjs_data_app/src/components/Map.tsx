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

export default function Map() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const [regionsVisible, setRegionsVisible] = useState(true);
  const [pointsVisible, setPointsVisible] = useState(true);

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
            'circle-radius': 8,
            'circle-color': '#f30',
            'circle-stroke-color': '#fff',
            'circle-stroke-width': 2
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
    </>
  );
}
