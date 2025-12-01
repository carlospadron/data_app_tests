# Flutter Data App

A Flutter-based data application using MapLibre GL for interactive map visualization.

## Prerequisites

- Flutter SDK installed
- VS Code with Flutter extension (recommended)
- Android Studio or Xcode for mobile development (optional)

## Getting Started

### 1. Verify Flutter Installation

Check your Flutter setup and environment:

```bash
flutter doctor
```

Resolve any issues reported by Flutter Doctor before proceeding.

### 2. Create a New Project

Create a new Flutter project through VS Code:

1. Open VS Code Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
2. Select **Flutter: New Project**
3. Choose **Application**
4. Select a directory and name your project

Alternatively, use the command line:

```bash
flutter create flutter_data_app
cd flutter_data_app
```

### 3. Add MapLibre GL Dependency

Add the MapLibre GL package to your project:

```bash
flutter pub add maplibre_gl
```

This will add the package to your `pubspec.yaml` and download dependencies.

## Configure Map Component

### 1. Update main.dart

Replace the content in `lib/main.dart` with a basic map setup:

```dart
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

  void _onMapCreated(MapLibreMapController controller) {
    mapController = controller;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: MapLibreMap(
        styleString: 'https://demotiles.maplibre.org/style.json',
        initialCameraPosition: const CameraPosition(
          target: LatLng(0.0, 0.0),
          zoom: 2.0,
        ),
        onMapCreated: _onMapCreated,
        myLocationEnabled: false,
        trackCameraPosition: true,
      ),
    );
  }
}
```

### 2. Configure Platform-Specific Settings

#### Android Configuration

Add internet permission to `android/app/src/main/AndroidManifest.xml`:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
    
    <application
        ...
    </application>
</manifest>
```

Update minimum SDK version in `android/app/build.gradle`:

```gradle
android {
    defaultConfig {
        minSdkVersion 21
        ...
    }
}
```

#### iOS Configuration

Add location permissions to `ios/Runner/Info.plist`:

```xml
<dict>
    ...
    <key>NSLocationWhenInUseUsageDescription</key>
    <string>This app needs access to location for map features.</string>
    <key>io.flutter.embedded_views_preview</key>
    <true/>
</dict>
```

Update minimum iOS version in `ios/Podfile`:

```ruby
platform :ios, '12.0'
```

#### Web Configuration

Add MapLibre GL JavaScript and CSS to `web/index.html` in the `<head>` section:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Flutter Data App</title>
  
  <!-- MapLibre GL JS -->
  <script src="https://unpkg.com/maplibre-gl@^4.3/dist/maplibre-gl.js"></script>
  <link href="https://unpkg.com/maplibre-gl@^4.3/dist/maplibre-gl.css" rel="stylesheet" />
  
  <link rel="manifest" href="manifest.json">
</head>
<body>
  <script src="flutter_bootstrap.js" async></script>
</body>
</html>
```

## Running the Application

### Development Mode

Run the application in development mode:

```bash
flutter run
```

### Additional Run Options

- **Select device**: `flutter run -d <device_id>`
- **Hot reload**: Press `r` in the terminal while running
- **Hot restart**: Press `R` in the terminal while running
- **List devices**: `flutter devices`

## Project Structure

```
flutter_data_app/
├── lib/
│   └── main.dart           # Application entry point with MapScreen
├── android/                 # Android-specific configuration
├── ios/                     # iOS-specific configuration
├── web/                     # Web-specific configuration
└── pubspec.yaml            # Dependencies and project configuration
```

## Additional Features

### Add Navigation Controls

To add zoom controls and compass, update the `MapLibreMap` widget:

```dart
MapLibreMap(
  styleString: 'https://demotiles.maplibre.org/style.json',
  initialCameraPosition: const CameraPosition(
    target: LatLng(0.0, 0.0),
    zoom: 2.0,
  ),
  onMapCreated: _onMapCreated,
  compassEnabled: true,
  logoViewMargins: const Point(10, 50),
)
```

### Add Markers

Add a marker to the map after it's created:

```dart
void _onMapCreated(MapLibreMapController controller) {
  mapController = controller;
  
  // Add a marker
  controller.addSymbol(
    SymbolOptions(
      geometry: const LatLng(0.0, 0.0),
      iconImage: 'marker-15',
      iconSize: 2.0,
    ),
  );
}
```

### Add Custom App Bar

Wrap the map with a Scaffold that includes an AppBar:

```dart
@override
Widget build(BuildContext context) {
  return Scaffold(
    appBar: AppBar(
      backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      title: const Text('Flutter Data App'),
    ),
    body: MapLibreMap(
      styleString: 'https://demotiles.maplibre.org/style.json',
      initialCameraPosition: const CameraPosition(
        target: LatLng(0.0, 0.0),
        zoom: 2.0,
      ),
      onMapCreated: _onMapCreated,
    ),
  );
}
```

### Handle Map Interactions

Add callbacks for user interactions:

```dart
MapLibreMap(
  styleString: 'https://demotiles.maplibre.org/style.json',
  initialCameraPosition: const CameraPosition(
    target: LatLng(0.0, 0.0),
    zoom: 2.0,
  ),
  onMapCreated: _onMapCreated,
  onMapClick: (point, latLng) {
    print('Map clicked at: ${latLng.latitude}, ${latLng.longitude}');
  },
  onCameraIdle: () {
    print('Camera stopped moving');
  },
)
```

## Build for Production

### Android APK

```bash
flutter build apk
```

The APK will be located at `build/app/outputs/flutter-apk/app-release.apk`

### iOS App

```bash
flutter build ios
```

Open the project in Xcode to create an archive for distribution.

### Web

```bash
flutter build web
```

The web build will be in the `build/web/` directory.

## Deployment

### Android

- Sign your APK/App Bundle
- Upload to Google Play Console
- See [Flutter deployment guide](https://docs.flutter.dev/deployment/android)

### iOS

- Configure signing in Xcode
- Create an archive
- Upload to App Store Connect
- See [Flutter deployment guide](https://docs.flutter.dev/deployment/ios)

### Web

Deploy the `build/web/` directory to:
- Firebase Hosting
- Netlify
- Vercel
- GitHub Pages

## Project Structure

```
flutter_data_app/
├── lib/
│   └── main.dart           # Application entry point with MapScreen
├── android/                 # Android-specific configuration
├── ios/                     # iOS-specific configuration
├── web/                     # Web-specific configuration
└── pubspec.yaml            # Dependencies and project configuration
```

## Resources

- [Flutter Documentation](https://docs.flutter.dev/get-started)
- [MapLibre GL Flutter Package](https://pub.dev/packages/maplibre_gl)
- [Flutter Samples](https://flutter.github.io/samples/)

## Development Tips

- Use hot reload for faster development iterations
- Run `flutter analyze` to check for code issues
- Format code with `flutter format .`
- Run tests with `flutter test`

## Troubleshooting

If you encounter issues:

1. Run `flutter doctor` to check your setup
2. Clear build cache: `flutter clean`
3. Reinstall dependencies: `flutter pub get`
4. Check the [Flutter GitHub issues](https://github.com/flutter/flutter/issues)