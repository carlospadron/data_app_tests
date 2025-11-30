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
lib/
├── main.dart           # Application entry point
├── screens/           # Screen widgets
├── widgets/           # Reusable UI components
└── models/            # Data models
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