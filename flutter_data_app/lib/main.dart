import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:maplibre_gl/maplibre_gl.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Data App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const MapScreen(),
    );
  }
}

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  MapLibreMapController? mapController;
  bool regionsVisible = true;
  bool pointsVisible = true;

  // Sample GeoJSON data
  final String regionsGeoJson = '''
  {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "properties": {"name": "Region A", "population": 50000},
        "geometry": {
          "type": "Polygon",
          "coordinates": [[
            [-10, 30], [10, 30], [10, 50], [-10, 50], [-10, 30]
          ]]
        }
      },
      {
        "type": "Feature",
        "properties": {"name": "Region B", "population": 75000},
        "geometry": {
          "type": "Polygon",
          "coordinates": [[
            [20, 10], [40, 10], [40, 30], [20, 30], [20, 10]
          ]]
        }
      }
    ]
  }
  ''';

  final String pointsGeoJson = '''
  {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "properties": {"name": "City A", "type": "Capital"},
        "geometry": {"type": "Point", "coordinates": [0, 40]}
      },
      {
        "type": "Feature",
        "properties": {"name": "City B", "type": "Major"},
        "geometry": {"type": "Point", "coordinates": [30, 20]}
      },
      {
        "type": "Feature",
        "properties": {"name": "City C", "type": "Minor"},
        "geometry": {"type": "Point", "coordinates": [-5, 35]}
      }
    ]
  }
  ''';

  void _onMapCreated(MapLibreMapController controller) {
    mapController = controller;
  }

  Future<void> _addGeoJsonLayers() async {
    if (mapController == null) return;

    try {
      // Add regions source and layers
      await mapController!.addSource(
        'regions',
        GeojsonSourceProperties(data: jsonDecode(regionsGeoJson)),
      );
      
      await mapController!.addLayer(
        'regions',
        'regions-fill',
        const FillLayerProperties(
          fillColor: '#088',
          fillOpacity: 0.4,
        ),
      );

      await mapController!.addLayer(
        'regions',
        'regions-outline',
        const LineLayerProperties(
          lineColor: '#088',
          lineWidth: 2.0,
        ),
      );

      // Add points source and layer
      await mapController!.addSource(
        'points',
        GeojsonSourceProperties(data: jsonDecode(pointsGeoJson)),
      );
      
      await mapController!.addLayer(
        'points',
        'points',
        const CircleLayerProperties(
          circleRadius: 8.0,
          circleColor: '#f30',
          circleStrokeColor: '#fff',
          circleStrokeWidth: 2.0,
        ),
      );
    } catch (e) {
      print('Error adding layers: $e');
    }
  }

  void _toggleRegions() async {
    setState(() {
      regionsVisible = !regionsVisible;
    });
    
    if (mapController != null) {
      await mapController!.setLayerVisibility(
        'regions-fill',
        regionsVisible,
      );
      await mapController!.setLayerVisibility(
        'regions-outline',
        regionsVisible,
      );
    }
  }

  void _togglePoints() async {
    setState(() {
      pointsVisible = !pointsVisible;
    });
    
    if (mapController != null) {
      await mapController!.setLayerVisibility(
        'points',
        pointsVisible,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          MapLibreMap(
            styleString: 'https://demotiles.maplibre.org/style.json',
            initialCameraPosition: const CameraPosition(
              target: LatLng(35.0, 15.0),
              zoom: 3.0,
            ),
            onMapCreated: _onMapCreated,
            onStyleLoadedCallback: _addGeoJsonLayers,
            myLocationEnabled: false,
            trackCameraPosition: true,
          ),
          Positioned(
            top: 10,
            left: 10,
            child: Container(
              padding: const EdgeInsets.all(15),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(4),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.3),
                    blurRadius: 4,
                    offset: const Offset(0, 2),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text(
                    'Layers',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 10),
                  Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Checkbox(
                        value: regionsVisible,
                        onChanged: (_) => _toggleRegions(),
                      ),
                      const Text('Regions'),
                    ],
                  ),
                  Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Checkbox(
                        value: pointsVisible,
                        onChanged: (_) => _togglePoints(),
                      ),
                      const Text('Points of Interest'),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}