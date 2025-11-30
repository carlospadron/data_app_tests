# Spatially-Enabled Data Apps Testing

A comprehensive evaluation of different technologies and frameworks for building spatially-enabled data applications. This repository contains prototypes and tests to compare various options for creating interactive map-based data visualization tools.

## Project Goal

Test and compare different technology stacks for building data applications with spatial/mapping capabilities, focusing on:

- **MapLibre GL integration** - Compatibility and ease of integration
- **Web deployment** - Ability to deploy as web applications
- **Development experience** - Language, ecosystem, and tooling
- **Cross-platform support** - Web, mobile, and desktop capabilities
- **Performance** - Rendering speed and resource usage

## Technology Categories

### Web Frameworks
- **Next.js** - React-based framework with SSR/SSG
- **Svelte** - Lightweight reactive framework
- **Vue** - Progressive JavaScript framework
- **Angular** - Full-featured TypeScript framework

### Multi-Platform Frameworks
- **Flutter** - Cross-platform framework using Dart
- **Kotlin Multiplatform** - JVM-based multiplatform solution

### Data App Frameworks
- **Streamlit** - Python-based data app framework
- **Shiny** - R/Python framework for data apps
- **Dash** - Python framework by Plotly
- **Panel** - Python visualization framework
- **Gradio** - ML-focused Python UI framework
- **Reflex** - Python full-stack framework
- **Taipy** - Python framework for data apps

### Analytics & Visualization Platforms
- **Observable** - JavaScript notebook platform
- **Evidence** - Business intelligence framework
- **Kepler.gl** - Geospatial data analysis tool

## Technologies Excluded from Testing

The following technologies were considered but excluded from testing for specific reasons:

### Game Engines
- **Unity, Unreal Engine, Godot** - These are designed for 3D game development and are overkill for 2D mapping applications. They have poor web performance, complex MapLibre GL integration challenges, and are not optimized for data-driven applications.

### Business Intelligence Tools
- **Power BI** - Closed Microsoft ecosystem with limited MapLibre integration and not designed for building custom spatial applications.
- **Grafana** - Optimized for time-series monitoring and observability, not general-purpose spatial data visualization.
- **Metabase, Apache Superset** - Business intelligence dashboarding tools with limited support for custom interactive map experiences.

### Not Web-Focused
- **Tauri** - Desktop and mobile only, no web deployment support which is a core requirement.

### Limited Scope
- **Voilà** - Simply converts Jupyter notebooks to web apps; not a framework for building production data applications.
- **Yew** - Rust WebAssembly framework adds unnecessary complexity for MapLibre GL integration compared to standard JavaScript frameworks.
- **Quarto** - Technical publishing and documentation system, not designed for interactive applications.

## Current Prototypes

### Web Framework Implementations

| Framework | Location | Status | Notes |
|-----------|----------|--------|-------|
| Next.js | `webgis_nextjs/` | ✅ Implemented | React-based, TypeScript |
| Next.js (Alt) | `webgis_nextjs_a/` | ✅ Implemented | Alternative implementation |
| Svelte | `webgis_svelte/` | ✅ Implemented | Lightweight, reactive |
| Vue | `webgis_vue/` | ✅ Implemented | Progressive framework |
| Flutter | - | 📋 Planned | See `FLUTTER.md` |

### Documentation

- `FLUTTER.md` - Flutter setup and integration guide
- `ANGULAR.md` - Angular implementation notes
- `NEXTJS.md` - Next.js implementation details
- `SVELTE.md` - Svelte implementation guide
- `VUE.md` - Vue.js implementation notes

## Evaluation Criteria

### MapLibre GL Compatibility
- **High** - Native JavaScript integration, straightforward
- **Medium** - Works but requires adapters or workarounds
- **Low** - Limited or no direct support

### Web Deployment
- Can the framework deploy to web browsers?
- Hosting options (static, SSR, edge functions)

### Language & Ecosystem
- Primary programming language
- Available libraries and community support
- Learning curve and developer experience

### UI Frameworks
- Built-in component libraries
- Customization capabilities
- Design system support

## Getting Started

Each prototype has its own README with specific setup instructions:

1. **Next.js**: See `webgis_nextjs/README.md`
2. **Svelte**: See `webgis_svelte/README.md`
3. **Vue**: See `webgis_vue/README.md`
4. **Flutter**: See `FLUTTER.md`

## Quick Start

```bash
# Next.js
cd webgis_nextjs
npm install
npm run dev

# Svelte
cd webgis_svelte
npm install
npm run dev

# Vue
cd webgis_vue
npm install
npm run dev
```

## Comparison Summary

See `comparison_of_options.csv` for a detailed feature comparison including:
- Framework category
- Web deployment capability
- Primary language
- MapLibre compatibility level
- Available UI frameworks
- Additional notes and considerations

## Contributing

This is a testing and evaluation repository. Each prototype demonstrates:
- Basic MapLibre GL map integration
- Interactive navigation components
- Framework-specific best practices

## License

See `LICENSE` file for details.

## Next Steps

- Complete Flutter implementation
- Add Python-based frameworks (Streamlit, Dash, Panel)
- Test performance benchmarks
- Document deployment strategies
- Add mobile platform tests