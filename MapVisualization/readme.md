### map-test.html should not be integrated with main
### map.html can be integrated with main

# Locations with Items Map

An interactive map visualization that displays rental item locations with filtering capabilities.

## What This Does

This page shows an interactive map of all locations that have rental items available. Users can:

- **View Locations on Map** - All locations with items are displayed as numbered markers (number = item count at that location)
- **Filter by Item** - Select a specific item to see only locations where that item is available
- **Filter by Availability** - Show only available or unavailable items
- **Hover for Details** - Hover over markers to see a tooltip listing all items at that location
  - Green highlighted items = Available
  - Red highlighted items = Not Available
- **Click for Info** - Click markers to see full location details
- **Open in Google Maps** - Click the button in popup to get directions to the location
- **Browse Location List** - Scrollable list below the map shows all filtered locations
- **View Statistics** - Dashboard shows total locations, items, cities, and states

## How It Works

1. **Loads Data** - Fetches Items, Users, and Locations from Supabase database
2. **Joins Tables** - Links Item → User → Location to find which locations have items
3. **Geocoding** - Converts addresses to GPS coordinates using Nominatim API (if not already in database)
4. **Displays Map** - Shows markers for each location with item count
5. **Interactive Filtering** - Filters update map, tooltips, and statistics in real-time

## Dependencies

All dependencies are loaded via CDN (no installation required):

- **Leaflet 1.9.4** - Interactive map library
- **Supabase JS 2.x** - Database client
- **Nominatim API** - OpenStreetMap geocoding service

## Usage

1. Open `map.html` in a web browser
2. Wait for locations to load and geocode (may take a few seconds)
3. Use filters to narrow down items
4. Hover over markers to see items
5. Click markers for full details and Google Maps link
6. Click locations in the list to zoom to them on map

