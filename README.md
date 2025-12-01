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
- **Streamlit** - Python-based data app framework with simple API
- **Dash** - Python framework by Plotly for analytical web apps
- **Panel** - Python framework for creating custom interactive dashboards
- **Reflex** - Python full-stack framework with React-like components

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
- **Gradio** - ML demo-focused framework with limited UI customization; too specialized for building rich spatial data applications.
- **Shiny** - Primarily R-focused (Python support secondary); better alternatives exist for Python-based spatial apps.
- **Taipy** - Newer framework with less mature ecosystem and limited MapLibre GL integration examples.
- **Kepler.gl** - Visualization component/tool, not a framework for building custom applications. Designed for geospatial data exploration rather than building full data apps.
- **Observable** - JavaScript notebook platform designed for data visualization and exploration, runs in browser only. Cannot write to databases without separate backend services. Better suited for prototyping than building full applications.
- **Evidence** - BI reporting tool focused on reading and displaying data via markdown/SQL. Not designed for transactional operations or database writes. Lacks the interactive form components needed for data entry applications.

## Current Prototypes

### Web Framework Implementations

**Note:** All web frameworks require foundational knowledge of HTML, CSS, and JavaScript/TypeScript. They also share common requirements including understanding of reactivity patterns, component lifecycle management, and API development for backend integration. The differences lie primarily in syntax, tooling, and architectural patterns.

| Framework | Location | Status | Setup Steps | Notes |
|-----------|----------|--------|-------------|-------|
| Next.js | `nextjs_data_app/` | ✅ Implemented | 5 | **Easy:** Create files in `src/components/`, use 'use client' for interactivity. Excellent TypeScript support, built-in routing. Strong ecosystem for future features. |
| Svelte | `svelte_data_app/` | ✅ Implemented | 4 | **Very Easy:** Create `.svelte` files in `src/lib/components/`. Minimal boilerplate, reactive by default. Svelte stores for state management. Clean, intuitive syntax for rapid development. |
| Vue | `vue_data_app/` | ✅ Implemented | 5 | **Easy:** Create `.vue` files in `src/components/`. Composition API provides flexible reactivity. Good balance of simplicity and power for scaling applications. |
| Angular | `angular_data_app/` | ✅ Implemented | 7 | **Moderate:** Use `ng generate component` CLI. More setup required (module imports, types). Enterprise-ready with comprehensive tooling. Best for large teams and complex apps. |
| Flutter | `flutter_data_app/` | ✅ Implemented | 6 | **Moderate:** Multi-platform (Web, Android, iOS). Requires platform-specific configs (permissions, minSDK, web index.html). Dart language. Hot reload for fast iteration. Strong for mobile-first apps. |

### Documentation

- `FLUTTER.md` - Flutter setup and integration guide
- `ANGULAR.md` - Angular implementation guide with MapLibre GL
- `NEXTJS.md` - Next.js comprehensive implementation guide
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

1. **Next.js**: See `NEXTJS.md`
2. **Svelte**: See `SVELTE.md`
3. **Vue**: See `VUE.md`
4. **Angular**: See `ANGULAR.md`
5. **Flutter**: See `FLUTTER.md`

## Quick Start

```bash
# Next.js
cd nextjs_data_app
npm install
npm run dev

# Svelte
cd svelte_data_app
npm install
npm run dev

# Vue
cd vue_data_app
npm install
npm run dev

# Angular
cd angular_data_app
npm install
ng serve
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
- Add Observable and Evidence implementations
- Test performance benchmarks across frameworks
- Document deployment strategies
- Compare bundle sizes and load times
- Add mobile platform tests