# Next.js Data App

A comprehensive guide for creating a spatially-enabled data application using Next.js and MapLibre GL.

## Prerequisites

- Node.js version 18.18.0 or higher
- npm or yarn package manager
- Basic knowledge of React and TypeScript

## Installation

### Create a New Project

Create a new Next.js application:

```bash
npx create-next-app@latest nextjs_data_app
```

When prompted, select the following options:
- **Would you like to use TypeScript?** → Yes
- **Would you like to use ESLint?** → Yes
- **Would you like to use Tailwind CSS?** → Yes (optional)
- **Would you like to use `src/` directory?** → Yes
- **Would you like to use App Router?** → Yes
- **Would you like to customize the default import alias?** → No

Navigate to the project directory:
```bash
cd nextjs_data_app
```

## Install MapLibre GL

Install MapLibre GL and its TypeScript types:

```bash
npm install maplibre-gl
```

The TypeScript types are included with the package.

## Configure Styles

Add MapLibre GL CSS to your global styles. Open `src/app/globals.css` and add at the top:

```css
@import 'maplibre-gl/dist/maplibre-gl.css';
```

## Create a Map Component

Create a new directory for components and add the map component:

```bash
mkdir -p src/components
```

Create `src/components/Map.tsx`:

```typescript
'use client';

import { useEffect, useRef } from 'react';
import maplibregl from 'maplibre-gl';

export default function Map() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);

  useEffect(() => {
    if (map.current) return; // Initialize map only once

    if (mapContainer.current) {
      map.current = new maplibregl.Map({
        container: mapContainer.current,
        style: 'https://demotiles.maplibre.org/style.json',
        center: [0, 0],
        zoom: 2
      });

      // Add navigation controls
      map.current.addControl(new maplibregl.NavigationControl(), 'top-right');
    }

    return () => {
      map.current?.remove();
    };
  }, []);

  return (
    <div 
      ref={mapContainer} 
      style={{ width: '100%', height: '100vh' }}
    />
  );
}
```

## Update App Page

Replace the content in `src/app/page.tsx`:

```typescript
import Map from '@/components/Map';

export default function Home() {
  return <Map />;
}
```

## Run the Application

Start the development server:

```bash
npm run dev
```

Open your browser and navigate to `http://localhost:3000`

## Project Structure

```
nextjs_data_app/
├── src/
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   └── components/
│       └── Map.tsx
├── next.config.ts
├── package.json
└── tsconfig.json
```

## Additional Features

### Add a Navigation Component

Create `src/components/Navigation.tsx`:

```typescript
'use client';

export default function Navigation() {
  return (
    <nav className="absolute top-0 left-0 right-0 bg-white shadow-md z-10 p-4">
      <h1 className="text-2xl font-bold">Data App</h1>
    </nav>
  );
}
```

Update `src/app/page.tsx` to include navigation:

```typescript
import Map from '@/components/Map';
import Navigation from '@/components/Navigation';

export default function Home() {
  return (
    <main>
      <Navigation />
      <Map />
    </main>
  );
}
```

### Add Markers

To add markers to your map, update the Map component:

```typescript
// Add after map initialization
new maplibregl.Marker()
  .setLngLat([0, 0])
  .addTo(map.current);
```

### Add Popup

```typescript
const popup = new maplibregl.Popup({ offset: 25 })
  .setText('Hello World!');

new maplibregl.Marker()
  .setLngLat([0, 0])
  .setPopup(popup)
  .addTo(map.current);
```

### Server-Side Rendering Considerations

Since MapLibre GL requires the browser environment, the Map component uses the `'use client'` directive. This ensures it only runs on the client side.

## Build for Production

Build the application:

```bash
npm run build
```

The build artifacts will be stored in the `.next/` directory.

Start the production server:

```bash
npm start
```

## Deployment

### Deploy to Vercel

Next.js is built by Vercel and deploys seamlessly:

```bash
npm install -g vercel
vercel
```

### Deploy to Other Platforms

Export as static site (if not using server features):

```bash
npm run build
```

The static files will be in the `.next` directory.

## Troubleshooting

### Map Not Displaying

1. Ensure MapLibre GL CSS is imported in `globals.css`
2. Check browser console for errors
3. Verify the map container has dimensions set

### TypeScript Errors

If you encounter TypeScript errors with MapLibre GL:

```bash
npm install --save-dev @types/maplibre-gl
```

### Build Errors

Clear the Next.js cache:

```bash
rm -rf .next
npm install
npm run build
```

## Performance Optimization

### Code Splitting

Next.js automatically code-splits by route. For further optimization, use dynamic imports:

```typescript
import dynamic from 'next/dynamic';

const Map = dynamic(() => import('@/components/Map'), {
  ssr: false,
  loading: () => <p>Loading map...</p>
});
```

### Image Optimization

Use Next.js Image component for optimized images:

```typescript
import Image from 'next/image';
```

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [MapLibre GL JS Documentation](https://maplibre.org/maplibre-gl-js/docs/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

## Next Steps

- Add data layers to the map
- Implement geospatial data visualization
- Create interactive controls and filters
- Add custom styling and theming
- Integrate with backend APIs for dynamic data
- Set up authentication and user management

