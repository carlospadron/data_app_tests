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

### Data App Frameworks
- **Streamlit** - Python-based data app framework with simple API
- **Dash** - Python framework by Plotly for analytical web apps
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

### IDE-Specific Requirements
- **Kotlin Multiplatform** - Requires IntelliJ IDEA or Android Studio for optimal development experience. While VS Code plugins exist, the tooling, debugging, and project setup heavily favor JetBrains IDEs, making it impractical for VS Code-centric workflows.

### Limited Scope
- **Voilà** - Simply converts Jupyter notebooks to web apps; not a framework for building production data applications.
- **Yew** - Rust WebAssembly framework adds unnecessary complexity for MapLibre GL integration compared to standard JavaScript frameworks.
- **Quarto** - Technical publishing and documentation system, not designed for interactive applications.
- **Gradio** - ML demo-focused framework with limited UI customization; too specialized for building rich spatial data applications.
- **Shiny** - Primarily R-focused (Python support secondary); better alternatives exist for Python-based spatial apps.
- **Taipy** - Newer framework with less mature ecosystem and limited MapLibre GL integration examples.
- **Panel** - Similar to Streamlit but less mature ecosystem. Streamlit and Dash already provide comprehensive Python data app coverage for different use cases (rapid prototyping vs. custom dashboards).
- **Kepler.gl** - Visualization component/tool, not a framework for building custom applications. Designed for geospatial data exploration rather than building full data apps.
- **Observable** - JavaScript notebook platform designed for data visualization and exploration, runs in browser only. Cannot write to databases without separate backend services. Better suited for prototyping than building full applications.
- **Evidence** - BI reporting tool focused on reading and displaying data via markdown/SQL. Not designed for transactional operations or database writes. Lacks the interactive form components needed for data entry applications.

## Current Prototypes

### Web & Multi-Platform Framework Implementations

**Note:** All web frameworks require foundational knowledge of HTML, CSS, and JavaScript/TypeScript. They also share common requirements including understanding of reactivity patterns, component lifecycle management, and API development for backend integration. The differences lie primarily in syntax, tooling, and architectural patterns.

| Framework | Type | Location | Status | Setup Steps | Notes |
|-----------|------|----------|--------|-------------|-------|
| Next.js | Web | `nextjs_data_app/` | ✅ Implemented | 5 | **Easy:** Create files in `src/components/`, use 'use client' for interactivity. Excellent TypeScript support, built-in routing. Strong ecosystem for future features. |
| Svelte | Web | `svelte_data_app/` | ✅ Implemented | 4 | **Very Easy:** Create `.svelte` files in `src/lib/components/`. Minimal boilerplate, reactive by default. Svelte stores for state management. Clean, intuitive syntax for rapid development. |
| Vue | Web | `vue_data_app/` | ✅ Implemented | 5 | **Easy:** Create `.vue` files in `src/components/`. Composition API provides flexible reactivity. Good balance of simplicity and power for scaling applications. |
| Angular | Web | `angular_data_app/` | ✅ Implemented | 7 | **Moderate:** Use `ng generate component` CLI. More setup required (module imports, types). Enterprise-ready with comprehensive tooling. Best for large teams and complex apps. |
| Flutter | Multi-Platform | `flutter_data_app/` | ✅ Implemented | 6 | **Moderate:** Multi-platform (Web, Android, iOS). Requires platform-specific configs (permissions, minSDK, web index.html). Dart language. Hot reload for fast iteration. Strong for mobile-first apps. |

### Python Data App Frameworks

| Framework | Location | Status | Setup Steps | Notes |
|-----------|----------|--------|-------------|-------|
| Streamlit | `streamlit_data_app/` | ✅ Implemented | 3 | **Very Easy:** PyDeck built-in, uses MapLibre GL JS natively. Reactive by default. Sidebar controls auto-refresh. Viewport state preserved across reruns. Perfect for rapid prototyping. |
| Dash | `dash_data_app/` | ✅ Implemented | 3 | **Easy:** Plotly-based with MapLibre GL JS rendering. Callback system for reactivity. More layout control than Streamlit. Good for custom dashboards. |
| Reflex | `reflex_data_app/` | ❌ **FAILED** | - | **Failed:** JavaScript integration issues. Scripts embedded via rx.script() or rx.html() do not execute reliably. Unable to initialize MapLibre GL despite multiple approaches. Not suitable for complex third-party JS library integration. |

### Documentation

- `ANGULAR.md` - Angular implementation guide with MapLibre GL
- `DASH.md` - Dash with Plotly implementation guide
- `FLUTTER.md` - Flutter setup and integration guide
- `NEXTJS.md` - Next.js comprehensive implementation guide
- `REFLEX.md` - Reflex full-stack Python implementation guide
- `STREAMLIT.md` - Streamlit with PyDeck implementation guide
- `SVELTE.md` - Svelte implementation guide
- `VUE.md` - Vue.js implementation notes

## Evaluation Results

### MapLibre GL Integration Comparison

| Framework | MapLibre Compatibility | Integration Method | Difficulty | GeoJSON Support |
|-----------|----------------------|-------------------|------------|----------------|
| Next.js | ⭐⭐⭐ High | Direct JS library import | Easy | Excellent |
| Svelte | ⭐⭐⭐ High | Direct JS library import | Very Easy | Excellent |
| Vue | ⭐⭐⭐ High | Direct JS library import | Easy | Excellent |
| Angular | ⭐⭐⭐ High | Direct JS library import | Moderate | Excellent |
| Flutter | ⭐⭐ Medium | maplibre_gl package | Moderate | Good (requires JSON parsing) |
| Streamlit | ⭐⭐⭐ High | PyDeck (MapLibre GL JS) | Very Easy | Excellent |
| Dash | ⭐⭐⭐ High | Plotly (MapLibre GL JS) | Easy | Excellent |
| Reflex | ❌ Failed | N/A | N/A | **Failed - Script execution issues** |

### Development Experience

| Framework | Setup Time | Learning Curve | Hot Reload | State Management | Code Verbosity |
|-----------|-----------|---------------|------------|------------------|----------------|
| Svelte | ~5 min | Low | ⚡ Instant | Reactive variables | Minimal |
| Next.js | ~8 min | Low-Medium | ⚡ Fast | React hooks | Low |
| Vue | ~8 min | Low-Medium | ⚡ Fast | Composition API | Low |
| Dash | ~5 min | Medium | 🔄 Moderate | Callbacks | Low-Medium |
| Reflex | ~8 min | Medium | ⚡ Fast | State class | Low-Medium |
| Streamlit | ~3 min | Very Low | ⚡ Fast | Auto-refresh | Minimal |
| Angular | ~15 min | Medium-High | 🔄 Moderate | Services/Signals | High |
| Flutter | ~10 min | Medium | ⚡ Fast | StatefulWidget | Medium |

### Layer Toggle Implementation Complexity

| Framework | Lines of Code | Implementation Approach |
|----------|--------------|---------------------|
| Streamlit | ~60 | Conditional layer creation in Python, sidebar checkboxes |
| Dash | ~95 | Plotly traces, callback decorator, checklist component |
| Svelte | ~160 | Reactive variables with bind:checked, simple toggle functions |
| Vue | ~165 | Composition API with refs, v-model binding |
| Next.js | ~185 | React hooks, inline styles |
| Angular | ~190 | TypeScript class, template with property binding |
| Flutter | ~200 | StatefulWidget with async layer visibility methods |
| Reflex | ❌ Failed | N/A - Script execution issues prevented completion |

### Deployment Options

| Framework | Static Export | SSR/SSG | Container | Edge Functions | Ease of Deployment |
|-----------|--------------|---------|-----------|----------------|-------------------|
| Next.js | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Vercel | ⭐⭐⭐ Excellent |
| Svelte | ✅ Yes | ✅ Yes (SvelteKit) | ✅ Yes | ✅ Vercel/Netlify | ⭐⭐⭐ Excellent |
| Vue | ✅ Yes | ✅ Yes (Nuxt) | ✅ Yes | ✅ Vercel/Netlify | ⭐⭐⭐ Excellent |
| Reflex | ❌ Failed | ❌ Failed | N/A | N/A | ❌ Test Failed |
| Dash | ❌ No | ❌ No | ✅ Yes | ❌ No | ⭐⭐ Good (Cloud/Docker) |
| Angular | ✅ Yes | ✅ Yes (Universal) | ✅ Yes | ⚠️ Limited | ⭐⭐ Good |
| Streamlit | ❌ No | ❌ No | ✅ Yes | ❌ No | ⭐⭐ Good (Cloud/Docker) |
| Flutter | ✅ Web only | ❌ No | ✅ Yes | ❌ No | ⭐ Fair |

### Key Findings

#### Best for Rapid Prototyping
1. **Streamlit** - Python-based, 3-minute setup, 60 lines, easiest overall
2. **Dash** - Python-based, 95 lines, good for Python developers who need more layout control
3. **Svelte** - JavaScript-based, minimal boilerplate, very intuitive for JS developers
4. **Vue** - JavaScript-based, clean syntax, good documentation

#### Best for Production Web Apps
1. **Next.js** - Full-featured, excellent ecosystem, strong deployment options
2. **Svelte** - Great performance, clean code, growing ecosystem
3. **Vue** - Mature, flexible, good balance of features

#### Best for Cross-Platform
1. **Flutter** - True multi-platform (Web/iOS/Android), but web performance varies

#### Best for Enterprise
1. **Angular** - Comprehensive tooling, strong typing, established patterns
2. **Next.js** - Strong ecosystem, great developer experience

#### MapLibre GL Integration Winner
**Tie: All frameworks except Flutter** - JavaScript frameworks (Svelte, Next.js, Vue, Angular) and Python frameworks (Streamlit, Dash) all have excellent native MapLibre GL JS integration. Flutter has medium compatibility requiring a package wrapper.

#### Simplest Implementation
**Streamlit** - 60 lines of Python, built-in PyDeck with MapLibre GL JS, automatic state management.

## Getting Started

Each prototype has its own README with specific setup instructions:

1. **Next.js**: See `NEXTJS.md`
2. **Svelte**: See `SVELTE.md`
3. **Vue**: See `VUE.md`
4. **Angular**: See `ANGULAR.md`
5. **Flutter**: See `FLUTTER.md`
6. **Streamlit**: See `STREAMLIT.md`
7. **Dash**: See `DASH.md`
8. **Reflex**: See `REFLEX.md` (⚠️ Test Failed)

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

# Flutter (Web)
cd flutter_data_app
flutter pub get
flutter run -d chrome

# Streamlit
cd streamlit_data_app
uv sync
uv run streamlit run app.py

# Dash
cd dash_data_app
uv sync
uv run python app.py

# Reflex (⚠️ FAILED - Not functional)
# cd reflex_data_app
# uv sync
# uv run reflex init
# uv run reflex run
```

## Contributing

This is a testing and evaluation repository. Each prototype demonstrates:
- Basic MapLibre GL map integration
- Two GeoJSON layers (sample regions and points of interest)
- Layer toggle menu for individual layer control
- Interactive navigation components
- Framework-specific best practices

## License
See `LICENSE` file for details.
Performance & Bundle Size
(To be added: Detailed performance benchmarks)

Future Work
Performance benchmarks (load time, FPS, memory usage)
Bundle size comparisons
Production deployment examples for each framework
Advanced MapLibre GL features (3D, clustering, custom styles)
Backend integration patterns
- **Full-Stack Apps**: Reflex (pure Python with React performance, 170 lines, state-based)
## Conclusions

### When Do You Actually Need JavaScript Web Frameworks?

**⚠️ Important:** For most data applications with modest user loads (<200 users), Python frameworks (Streamlit, Dash) are sufficient and significantly simpler.

**Stick with Python Frameworks (Streamlit/Dash) if:**
- User base: <200 concurrent users
- Use case: Internal tools, dashboards, data exploration
- UI needs: Standard controls, charts, maps are sufficient
- Team: Python developers who want to stay in Python
- Priority: Fast development and maintenance

**Consider JavaScript Frameworks (Next.js/Svelte/Vue) when:**
- **Complex UI Requirements:**
  - Heavy real-time collaboration (multiple users editing simultaneously)
  - Complex drag-and-drop interactions
  - Custom animations and transitions
  - Offline-first applications
  - Very custom UI/UX not achievable with standard components

- **High Traffic/Performance Needs:**
  - Thousands of concurrent users
  - Need for static site generation (SSG) for performance
  - Edge deployment requirements
  - Mobile app-like experience required

- **Public-Facing Applications:**
  - SEO-critical content
  - Public website with marketing pages
  - E-commerce or consumer-facing apps

- **Team/Ecosystem Requirements:**
  - Team has JavaScript/TypeScript expertise
  - Need to integrate with complex frontend ecosystem
  - Building a product that will scale to enterprise complexity

**Bottom Line:** Don't choose Next.js/Svelte/Vue just because they're "modern" or "better" - they add significant complexity. Choose them when Streamlit/Dash actually can't deliver the UX you need or handle your scale.

---

### Recommended Framework by Use Case

**For Python Developers:**
- **Quick Prototyping**: Streamlit (simplest, 60 lines, automatic state management)
- **Custom Dashboards**: Dash (more layout control, 95 lines, callback-based reactivity)
- **⚠️ Not Recommended**: Reflex (failed - JavaScript integration issues prevent third-party library usage)

**For JavaScript Developers:**
- **Rapid Development**: Svelte (minimal boilerplate, very intuitive)
- **Modern Web Apps**: Next.js or Svelte (excellent DX, strong deployment)
- **Enterprise Applications**: Angular or Next.js (comprehensive tooling)
- **Team Flexibility**: Vue (good balance, easy to learn)

**For Multi-Platform:**
- **Mobile + Web**: Flutter (with caveats on web performance)

### MapLibre GL Integration Success

**Successful Integrations:**
- **JavaScript frameworks** (Svelte, Next.js, Vue, Angular) have native, straightforward integration
- **Python frameworks** (Streamlit via PyDeck, Dash via Plotly) use MapLibre GL JS natively
- **Flutter** requires a package but works well across platforms

**Failed Integration:**
- **Reflex** - Unable to reliably execute embedded JavaScript. Multiple approaches attempted (rx.script(), rx.html(), component-based) all failed. The React compilation layer interferes with direct script execution, making third-party JS library integration impractical.

**Note:** Plotly switched from Mapbox GL JS to MapLibre GL JS, eliminating the need for API tokens.

### Performance & Bundle Size

*(To be added: Detailed performance benchmarks)*

## Future Work

- Add table and sync selection with map
- Performance benchmarks (load time, FPS, memory usage)
- Bundle size comparisons
- Production deployment examples for each framework
- Advanced MapLibre GL features (3D, clustering, custom styles)
- Backend integration patterns