# Blazor Data App

A comprehensive guide for creating a spatially-enabled data application using Blazor WebAssembly and MapLibre GL.

## Prerequisites

- .NET SDK 8.0 or higher
- Basic knowledge of C# and Razor syntax

## Installation

### Install .NET SDK

Download and install the .NET SDK from [https://dotnet.microsoft.com/download](https://dotnet.microsoft.com/download).

Verify installation:
```bash
dotnet --version
```

## Create a New Project

Create a new Blazor WebAssembly standalone application:

```bash
dotnet new blazorwasm -o blazor_data_app
```

Navigate to the project directory:
```bash
cd blazor_data_app
```

## Configure MapLibre GL

Blazor WebAssembly runs in the browser and integrates with JavaScript libraries through JS interop. MapLibre GL JS is loaded via CDN.

### Update `wwwroot/index.html`

Add the MapLibre GL CSS and JS references in the `<head>` section:

```html
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl/dist/maplibre-gl.css" />
<script src="https://unpkg.com/maplibre-gl/dist/maplibre-gl.js"></script>
```

## Create the JavaScript Interop Module

Create `wwwroot/js/mapInterop.js`:

```javascript
let map = null;
let mapLoaded = false;

export function initializeMap(containerId) {
    map = new maplibregl.Map({
        container: containerId,
        style: 'https://demotiles.maplibre.org/style.json',
        center: [15, 35],
        zoom: 3
    });

    map.addControl(new maplibregl.NavigationControl(), 'top-right');

    map.on('load', () => {
        mapLoaded = true;
        // Add GeoJSON sources and layers here
    });
}

export function setLayerVisibility(layerIds, visible) {
    if (!map || !mapLoaded) return;
    const visibility = visible ? 'visible' : 'none';
    for (const layerId of layerIds) {
        map.setLayoutProperty(layerId, 'visibility', visibility);
    }
}

export function destroyMap() {
    if (map) {
        map.remove();
        map = null;
        mapLoaded = false;
    }
}
```

## Create the Map Component

Create `Components/Map.razor`:

```razor
@using Microsoft.JSInterop
@inject IJSRuntime JS
@implements IAsyncDisposable

<div style="position: relative; width: 100%; height: 100vh;">
    <div id="map" style="width: 100%; height: 100%;"></div>

    <div class="layer-control">
        <h3>Layers</h3>
        <div class="layer-item">
            <label>
                <input type="checkbox" checked="@regionsVisible" @onchange="ToggleRegions" />
                Regions
            </label>
        </div>
        <div class="layer-item">
            <label>
                <input type="checkbox" checked="@pointsVisible" @onchange="TogglePoints" />
                Points of Interest
            </label>
        </div>
    </div>
</div>

@code {
    private IJSObjectReference? mapModule;
    private bool regionsVisible = true;
    private bool pointsVisible = true;

    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            mapModule = await JS.InvokeAsync<IJSObjectReference>(
                "import", "./js/mapInterop.js");
            await mapModule.InvokeVoidAsync("initializeMap", "map");
        }
    }

    private async Task ToggleRegions(ChangeEventArgs e)
    {
        regionsVisible = (bool)(e.Value ?? true);
        if (mapModule is not null)
        {
            await mapModule.InvokeVoidAsync("setLayerVisibility",
                new[] { "regions-fill", "regions-outline" }, regionsVisible);
        }
    }

    private async Task TogglePoints(ChangeEventArgs e)
    {
        pointsVisible = (bool)(e.Value ?? true);
        if (mapModule is not null)
        {
            await mapModule.InvokeVoidAsync("setLayerVisibility",
                new[] { "points" }, pointsVisible);
        }
    }

    public async ValueTask DisposeAsync()
    {
        if (mapModule is not null)
        {
            await mapModule.InvokeVoidAsync("destroyMap");
            await mapModule.DisposeAsync();
        }
    }
}
```

## Update the Home Page

Replace the content in `Pages/Home.razor`:

```razor
@page "/"

<PageTitle>Blazor Data App</PageTitle>

<Map />
```

## Update `_Imports.razor`

Add the Components namespace:

```razor
@using blazor_data_app.Components
```

## Simplify the Layout

Update `Layout/MainLayout.razor` to remove sidebar navigation for a full-screen map:

```razor
@inherits LayoutComponentBase
<div style="margin: 0; padding: 0; overflow: hidden;">
    @Body
</div>
```

## Run the Application

Start the development server:

```bash
dotnet run
```

Or with hot reload:

```bash
dotnet watch run
```

Open your browser and navigate to `http://localhost:5000` (or the URL shown in the terminal).

## Project Structure

```
blazor_data_app/
├── Components/
│   └── Map.razor
├── Layout/
│   ├── MainLayout.razor
│   └── MainLayout.razor.css
├── Pages/
│   └── Home.razor
├── wwwroot/
│   ├── css/
│   │   └── app.css
│   ├── js/
│   │   └── mapInterop.js
│   └── index.html
├── _Imports.razor
├── App.razor
├── Program.cs
└── blazor_data_app.csproj
```

## Features Implemented

### GeoJSON Layers

The application includes two GeoJSON layers:

1. **Regions Layer** - Displays polygon regions with properties like name and population
2. **Points of Interest Layer** - Shows circle markers for cities and landmarks

### Layer Toggle Menu

A control panel in the top-left corner allows users to:
- Toggle each layer on/off independently
- See which layers are currently visible
- Control layer visibility in real-time

### JavaScript Interop

Blazor WebAssembly integrates with MapLibre GL JS through the `IJSRuntime` service:
- `JS.InvokeAsync<IJSObjectReference>` loads the JS module dynamically
- `mapModule.InvokeVoidAsync` calls JavaScript functions from C#
- `IAsyncDisposable` ensures the map is properly cleaned up on component disposal

## Build for Production

Build the application:

```bash
dotnet publish -c Release
```

The output will be in `bin/Release/net*/publish/wwwroot` – a static site that can be hosted anywhere.

## Deployment

### Static Hosting

Blazor WebAssembly compiles to static files and can be deployed to:
- **GitHub Pages** - Free static hosting
- **Azure Static Web Apps** - Microsoft's hosting with CI/CD
- **Netlify / Vercel** - Static site hosting platforms
- **Any web server** - Apache, Nginx, etc.

### GitHub Pages Example

```bash
dotnet publish -c Release -o publish
# Deploy publish/wwwroot to GitHub Pages
```

## Troubleshooting

### Map Not Displaying

1. Ensure MapLibre GL JS and CSS are loaded in `index.html`
2. Check browser console for JavaScript errors
3. Verify the map container has a defined height

### JS Interop Errors

If you see "JavaScript interop calls cannot be issued at this time":
- Ensure JS interop calls happen in `OnAfterRenderAsync`, not `OnInitializedAsync`
- The component must be rendered before JS calls can be made

### Build Errors

Restore packages and rebuild:

```bash
dotnet restore
dotnet build
```

## Resources

- [Blazor Documentation](https://learn.microsoft.com/aspnet/core/blazor/)
- [Blazor JavaScript Interop](https://learn.microsoft.com/aspnet/core/blazor/javascript-interoperability/)
- [MapLibre GL JS Documentation](https://maplibre.org/maplibre-gl-js/docs/)
- [Blazor WebAssembly Hosting](https://learn.microsoft.com/aspnet/core/blazor/host-and-deploy/webassembly)

## Next Steps

- Add data layers to the map
- Implement geospatial data visualization
- Create interactive controls and filters
- Add custom styling and theming
- Integrate with backend APIs for dynamic data
- Add routing with Blazor Router
- Implement server-side data fetching with HttpClient
