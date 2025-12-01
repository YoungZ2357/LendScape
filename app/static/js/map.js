
let map;
let markers = [];
let locationsWithItems = [];
let filteredLocations = [];
let allItems = [];
let allUsers = [];
let allLocations = [];

async function init() {
    await loadLocationsWithItems();
}

async function loadLocationsWithItems() {
    try {
        document.getElementById('mapLoading').innerHTML = 'Loading data from server...';

        const [itemsResponse, usersResponse, locationsResponse] = await Promise.all([
            fetch('/api/items/all'),
            fetch('/api/users/all'),
            fetch('/api/locations/all')
        ]);

        if (!itemsResponse.ok || !usersResponse.ok || !locationsResponse.ok) {
            throw new Error('Failed to fetch data from server');
        }

        const itemsData = await itemsResponse.json();
        const usersData = await usersResponse.json();
        const locationsData = await locationsResponse.json();

        // 提取数据
        allItems = itemsData.items || itemsData.results || itemsData || [];
        allUsers = usersData.users || usersData.results || usersData || [];
        allLocations = locationsData.locations || locationsData.results || locationsData || [];

        console.log('=== Data loaded ===');
        console.log('Items:', allItems.length);
        console.log('Users:', allUsers.length);
        console.log('Locations:', allLocations.length);

        const locationIdsWithItems = new Set();
        const itemCountByLocation = {};

        allItems.forEach(item => {
            const user = allUsers.find(u => u.userId === item.userId);
            if (user && user.locationId) {
                locationIdsWithItems.add(user.locationId);
                itemCountByLocation[user.locationId] = (itemCountByLocation[user.locationId] || 0) + 1;
            }
        });

        console.log('Locations with items:', locationIdsWithItems.size);

        const locationsToGeocode = allLocations.filter(loc =>
            locationIdsWithItems.has(loc.locationId)
        );

        console.log('Locations to geocode:', locationsToGeocode.length);

        const geocodedLocations = [];

        for (let i = 0; i < locationsToGeocode.length; i++) {
            const location = locationsToGeocode[i];

            document.getElementById('mapLoading').innerHTML =
                `Geocoding location ${i + 1} of ${locationsToGeocode.length}...<br>` +
                `<small>${location.city || 'Unknown'}, ${location.state || ''}</small>`;

            if (location.latitude && location.longitude) {
                geocodedLocations.push({
                    ...location,
                    itemCount: itemCountByLocation[location.locationId]
                });
            } else {
                const coords = await geocodeAddress(location);
                if (coords) {
                    geocodedLocations.push({
                        ...location,
                        latitude: coords.latitude,
                        longitude: coords.longitude,
                        itemCount: itemCountByLocation[location.locationId]
                    });


                } else {
                    geocodedLocations.push({
                        ...location,
                        itemCount: itemCountByLocation[location.locationId]
                    });
                }

                if (i < locationsToGeocode.length - 1) {
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }
            }
        }

        locationsWithItems = geocodedLocations;
        filteredLocations = [...locationsWithItems];

        // 初始化界面
        populateFilters();
        updateStats();
        initMap();
        displayMarkers(filteredLocations);
        displayLocationList(filteredLocations);

    } catch (err) {
        console.error('Load error:', err);
        showError(`Error loading data: ${err.message}`);
    }
}

async function geocodeAddress(location) {
    try {
        const strategies = [
            [location.address, location.city, location.state, location.postcode, location.country].filter(Boolean).join(', '),
            [location.city, location.state, location.postcode, location.country].filter(Boolean).join(', '),
            [location.city, location.state, location.country].filter(Boolean).join(', ')
        ];

        for (let i = 0; i < strategies.length; i++) {
            const query = strategies[i];
            console.log(`Geocoding attempt ${i + 1}:`, query);

            try {
                const response = await fetch(
                    `https://nominatim.openstreetmap.org/search?` +
                    `format=json&q=${encodeURIComponent(query)}&limit=1`,
                    {
                        headers: { 'User-Agent': 'LendScapeMap/1.0' }
                    }
                );

                if (response.ok) {
                    const results = await response.json();
                    if (results && results.length > 0) {
                        console.log(`✓ Success with strategy ${i + 1}`);
                        return {
                            latitude: parseFloat(results[0].lat),
                            longitude: parseFloat(results[0].lon)
                        };
                    }
                }
            } catch (err) {
                console.warn(`Strategy ${i + 1} failed:`, err);
            }

            await new Promise(resolve => setTimeout(resolve, 500));
        }

        console.warn(`All strategies failed for ${location.city}`);
        return null;
    } catch (err) {
        console.error('Geocoding error:', err);
        return null;
    }
}



function populateFilters() {
    const uniqueItems = [...new Set(allItems
        .filter(i => i.itemName)
        .map(i => JSON.stringify({ id: i.itemId, name: i.itemName }))
    )].map(s => JSON.parse(s));

    const itemSelect = document.getElementById('itemFilter');
    uniqueItems.forEach(item => {
        const option = document.createElement('option');
        option.value = item.id;
        option.textContent = item.name;
        itemSelect.appendChild(option);
    });

    itemSelect.addEventListener('change', applyFilters);
    document.getElementById('availabilityFilter').addEventListener('change', applyFilters);
}

function applyFilters() {
    const itemId = document.getElementById('itemFilter').value;
    const availability = document.getElementById('availabilityFilter').value;


    let filteredItems = allItems;

    if (itemId) {
        filteredItems = filteredItems.filter(item => item.itemId == itemId);
    }

    if (availability) {
        filteredItems = filteredItems.filter(item =>
            item.is_available === (availability === 'true')
        );
    }


    const locationIdsWithFilteredItems = new Set();
    const itemCountByLocation = {};

    filteredItems.forEach(item => {
        const user = allUsers.find(u => u.userId === item.userId);
        if (user && user.locationId) {
            locationIdsWithFilteredItems.add(user.locationId);
            itemCountByLocation[user.locationId] = (itemCountByLocation[user.locationId] || 0) + 1;
        }
    });

    filteredLocations = locationsWithItems.filter(loc =>
        locationIdsWithFilteredItems.has(loc.locationId)
    ).map(loc => ({
        ...loc,
        itemCount: itemCountByLocation[loc.locationId]
    }));

    displayMarkers(filteredLocations);
    displayLocationList(filteredLocations);
    updateStats();
}

function resetFilters() {
    document.getElementById('itemFilter').value = '';
    document.getElementById('availabilityFilter').value = '';

    const itemCountByLocation = {};
    allItems.forEach(item => {
        const user = allUsers.find(u => u.userId === item.userId);
        if (user && user.locationId) {
            itemCountByLocation[user.locationId] = (itemCountByLocation[user.locationId] || 0) + 1;
        }
    });

    filteredLocations = locationsWithItems.map(loc => ({
        ...loc,
        itemCount: itemCountByLocation[loc.locationId]
    }));

    displayMarkers(filteredLocations);
    displayLocationList(filteredLocations);
    updateStats();
}

function initMap() {
    document.getElementById('mapLoading').style.display = 'none';
    document.getElementById('map').style.display = 'block';

    // 初始化地图，中心设在波士顿
    map = L.map('map').setView([42.3601, -71.0589], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18
    }).addTo(map);
}

function displayMarkers(locations) {
    markers.forEach(m => map.removeLayer(m));
    markers = [];

    const validLocations = locations.filter(loc =>
        loc.latitude && loc.longitude &&
        !isNaN(loc.latitude) && !isNaN(loc.longitude)
    );

    if (validLocations.length === 0) {
        console.warn('No valid coordinates to display');
        return;
    }

    validLocations.forEach(loc => {
        const icon = L.divIcon({
            className: 'custom-marker',
            html: `<div style="
                background-color: #667eea;
                width: 35px;
                height: 35px;
                border-radius: 50%;
                border: 3px solid white;
                box-shadow: 0 3px 6px rgba(0,0,0,0.3);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                font-size: 14px;
            ">${loc.itemCount}</div>`,
            iconSize: [35, 35],
            iconAnchor: [17, 17],
            popupAnchor: [0, -17]
        });

        const itemsAtLocation = allItems.filter(item => {
            const user = allUsers.find(u => u.userId === item.userId);
            return user && user.locationId === loc.locationId;
        });

        const popupHtml = `
            <div style="padding: 10px; min-width: 250px;">
                <h3 style="margin: 0 0 10px 0; color: #1f2937;">${loc.city || 'Unknown City'}</h3>
                <p style="margin: 5px 0; color: #6b7280;">
                    <strong>Address:</strong> ${loc.address || 'N/A'}<br>
                    <strong>State:</strong> ${loc.state || 'N/A'}<br>
                    <strong>Items:</strong> ${loc.itemCount}
                </p>
                <div style="margin-top: 12px;">
                    <h4 style="margin: 0 0 8px 0; color: #4b5563;">Available Items:</h4>
                    ${itemsAtLocation.slice(0, 5).map(item => `
                        <div style="padding: 4px 0; border-bottom: 1px solid #e5e7eb;">
                            <strong>${item.itemName}</strong> - $${item.price || '0'}
                            ${item.is_available ?
            '<span style="color: #10b981; font-size: 12px;"> ✓ Available</span>' :
            '<span style="color: #ef4444; font-size: 12px;"> ✗ Rented</span>'}
                        </div>
                    `).join('')}
                    ${itemsAtLocation.length > 5 ?
            `<p style="margin-top: 8px; color: #9ca3af; font-size: 12px;">
                            +${itemsAtLocation.length - 5} more items
                        </p>` : ''}
                </div>
                <div style="margin-top: 12px; text-align: center;">
                    <a href="https://www.google.com/maps?q=${loc.latitude},${loc.longitude}" 
                       target="_blank" 
                       style="display: inline-block; padding: 8px 16px; background: #4285f4; 
                              color: white; text-decoration: none; border-radius: 6px; 
                              font-weight: 600; font-size: 13px;">
                        📍 Open in Google Maps
                    </a>
                </div>
            </div>
        `;

        const marker = L.marker([loc.latitude, loc.longitude], { icon })
            .addTo(map)
            .bindPopup(popupHtml, { maxWidth: 300 });

        markers.push(marker);
    });

    if (markers.length > 0) {
        const group = L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.1));
    }
}

function updateStats() {
    document.getElementById('totalLocations').textContent = filteredLocations.length;

    const totalFilteredItems = filteredLocations.reduce((sum, loc) => sum + loc.itemCount, 0);
    document.getElementById('totalItems').textContent = totalFilteredItems;

    const uniqueCities = new Set(filteredLocations.map(l => l.city).filter(Boolean));
    document.getElementById('uniqueCities').textContent = uniqueCities.size;

    const uniqueStates = new Set(filteredLocations.map(l => l.state).filter(Boolean));
    document.getElementById('uniqueStates').textContent = uniqueStates.size;
}

function displayLocationList(locations) {
    const listContainer = document.getElementById('locationList');
    const listContent = document.getElementById('listContent');

    if (locations.length === 0) {
        listContainer.style.display = 'none';
        return;
    }

    listContainer.style.display = 'block';
    listContent.innerHTML = '';

    locations.forEach(loc => {
        const item = document.createElement('div');
        item.className = 'location-item';
        item.innerHTML = `
            <strong>${loc.city || 'Unknown'}, ${loc.state || 'N/A'}</strong>
            <span class="item-count">${loc.itemCount} items</span>
            <small style="display: block; margin-top: 4px; color: #6b7280;">
                ${loc.address || 'No address'}
            </small>
        `;

        item.onclick = () => {
            if (loc.latitude && loc.longitude) {
                map.setView([loc.latitude, loc.longitude], 15);
                const marker = markers.find(m =>
                    m.getLatLng().lat === loc.latitude &&
                    m.getLatLng().lng === loc.longitude
                );
                if (marker) {
                    marker.openPopup();
                }
            }
        };

        listContent.appendChild(item);
    });
}

function showError(message) {
    const mapContainer = document.querySelector('.map-container');
    mapContainer.innerHTML = `
        <div style="background: #fee2e2; border: 1px solid #fecaca; color: #991b1b; 
                    padding: 20px; border-radius: 8px; margin: 20px; text-align: center;">
            ${message}
        </div>
    `;
}

window.onload = init;