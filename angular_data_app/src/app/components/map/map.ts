import { Component, OnInit, OnDestroy } from '@angular/core';
import * as maplibregl from 'maplibre-gl';

@Component({
  selector: 'app-map',
  imports: [],
  templateUrl: './map.html',
  styleUrl: './map.css',
})
export class Map implements OnInit, OnDestroy {
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
