/**
 * European Train Routes Explorer
 * JavaScript for the interactive train routes map
 */

// Global variables
let map;
let trainData = null;
let stations = [];
let connections = {};
let markers = {};
let routeLines = [];
let selectedStation = null;

// Map configuration
const defaultMapCenter = [48.8566, 2.3522]; // Paris coordinates
const defaultZoom = 5;
const stationIcon = L.divIcon({
  className: 'station-marker',
  html: '<div class="station-dot"></div>',
  iconSize: [12, 12],
  iconAnchor: [6, 6]
});

// Colors for different railway operators
const operatorColors = {
  'Deutsche Bahn': '#ff0000',
  'SNCF': '#0000ff',
  'Trenitalia': '#00aa00',
  'International': '#ff9900',
  'default': '#999999'
};

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
  initMap();
  loadData();
  setupEventListeners();
});

// Initialize the Leaflet map
function initMap() {
  map = L.map('map').setView(defaultMapCenter, defaultZoom);
  
  // Add OpenStreetMap tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 18
  }).addTo(map);
  
  // Add a scale control
  L.control.scale().addTo(map);
}

// Load train data from the JSON file
function loadData() {
  // Load from the data directory
  fetch('./data/web_data.json')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      trainData = data;
      stations = data.stations;
      connections = data.connections;
      
      // Update statistics
      document.getElementById('total-stations').textContent = stations.length;
      
      // Count total routes
      let totalRoutes = 0;
      Object.keys(connections).forEach(station => {
        totalRoutes += connections[station].length;
      });
      document.getElementById('total-routes').textContent = totalRoutes;
      
      // Add all stations to the map
      addAllStationsToMap();
      
      // Initialize search functionality
      initializeSearch();
    })
    .catch(error => {
      console.error('Error loading train data:', error);
      
      // For development/demonstration, use placeholder data if fetch fails
      usePlaceholderData();
    });
}

// Use placeholder data for development/demonstration
function usePlaceholderData() {
  console.log('Using placeholder data for development');
  
  // Create placeholder stations (major European cities)
  const placeholderStations = [
    { name: "Paris Gare du Nord", latitude: 48.8809, longitude: 2.3553 },
    { name: "London St Pancras", latitude: 51.5322, longitude: -0.1271 },
    { name: "Brussels Midi", latitude: 50.8357, longitude: 4.3356 },
    { name: "Amsterdam Centraal", latitude: 52.3789, longitude: 4.9003 },
    { name: "Berlin Hauptbahnhof", latitude: 52.5250, longitude: 13.3690 },
    { name: "Frankfurt Hauptbahnhof", latitude: 50.1071, longitude: 8.6636 },
    { name: "München Hauptbahnhof", latitude: 48.1402, longitude: 11.5600 },
    { name: "Zürich Hauptbahnhof", latitude: 47.3783, longitude: 8.5403 },
    { name: "Milano Centrale", latitude: 45.4862, longitude: 9.2050 },
    { name: "Roma Termini", latitude: 41.9010, longitude: 12.5011 }
  ];
  
  // Create placeholder connections
  const placeholderConnections = {
    "Paris Gare du Nord": [
      { name: "London St Pancras", latitude: 51.5322, longitude: -0.1271, operator: "International", country: "France-UK" },
      { name: "Brussels Midi", latitude: 50.8357, longitude: 4.3356, operator: "International", country: "France-Belgium" },
      { name: "Amsterdam Centraal", latitude: 52.3789, longitude: 4.9003, operator: "International", country: "France-Netherlands" }
    ],
    "London St Pancras": [
      { name: "Paris Gare du Nord", latitude: 48.8809, longitude: 2.3553, operator: "International", country: "UK-France" },
      { name: "Brussels Midi", latitude: 50.8357, longitude: 4.3356, operator: "International", country: "UK-Belgium" }
    ],
    "Brussels Midi": [
      { name: "Paris Gare du Nord", latitude: 48.8809, longitude: 2.3553, operator: "International", country: "Belgium-France" },
      { name: "Amsterdam Centraal", latitude: 52.3789, longitude: 4.9003, operator: "International", country: "Belgium-Netherlands" },
      { name: "Frankfurt Hauptbahnhof", latitude: 50.1071, longitude: 8.6636, operator: "International", country: "Belgium-Germany" }
    ],
    "Berlin Hauptbahnhof": [
      { name: "Frankfurt Hauptbahnhof", latitude: 50.1071, longitude: 8.6636, operator: "Deutsche Bahn", country: "Germany" },
      { name: "München Hauptbahnhof", latitude: 48.1402, longitude: 11.5600, operator: "Deutsche Bahn", country: "Germany" }
    ],
    "Milano Centrale": [
      { name: "Zürich Hauptbahnhof", latitude: 47.3783, longitude: 8.5403, operator: "International", country: "Italy-Switzerland" },
      { name: "Roma Termini", latitude: 41.9010, longitude: 12.5011, operator: "Trenitalia", country: "Italy" }
    ]
  };
  
  stations = placeholderStations;
  connections = placeholderConnections;
  
  // Update statistics
  document.getElementById('total-stations').textContent = stations.length;
  
  // Count total routes
  let totalRoutes = 0;
  Object.keys(connections).forEach(station => {
    totalRoutes += connections[station].length;
  });
  document.getElementById('total-routes').textContent = totalRoutes;
  
  // Add all stations to the map
  addAllStationsToMap();
  
  // Initialize search functionality
  initializeSearch();
}

// Add all stations to the map as markers
function addAllStationsToMap() {
  stations.forEach(station => {
    const marker = L.marker([station.latitude, station.longitude], {
      title: station.name,
      icon: stationIcon
    }).addTo(map);
    
    marker.bindTooltip(station.name);
    
    // Store the marker reference
    markers[station.name] = marker;
    
    // Add click event to the marker
    marker.on('click', () => {
      selectStation(station.name);
      showConnectionsForStation(station.name);
    });
  });
}

// Initialize the station search functionality
function initializeSearch() {
  const searchInput = document.getElementById('station-search');
  const suggestionsContainer = document.getElementById('station-suggestions');
  const searchBtn = document.getElementById('search-btn');
  
  // Setup autocomplete for station search
  searchInput.addEventListener('input', () => {
    const searchTerm = searchInput.value.toLowerCase();
    
    // Clear suggestions
    suggestionsContainer.innerHTML = '';
    
    if (searchTerm.length < 2) {
      suggestionsContainer.style.display = 'none';
      return;
    }
    
    // Filter stations based on search term
    const matchingStations = stations.filter(station => 
      station.name.toLowerCase().includes(searchTerm)
    );
    
    // Display matching stations
    if (matchingStations.length > 0) {
      suggestionsContainer.style.display = 'block';
      
      matchingStations.forEach(station => {
        const div = document.createElement('div');
        div.textContent = station.name;
        div.addEventListener('click', () => {
          searchInput.value = station.name;
          suggestionsContainer.style.display = 'none';
          selectStation(station.name);
        });
        suggestionsContainer.appendChild(div);
      });
    } else {
      suggestionsContainer.style.display = 'none';
    }
  });
  
  // Handle search button click
  searchBtn.addEventListener('click', () => {
    const searchTerm = searchInput.value;
    if (searchTerm && stations.some(s => s.name === searchTerm)) {
      selectStation(searchTerm);
    }
  });
  
  // Hide suggestions when clicking outside
  document.addEventListener('click', (e) => {
    if (e.target !== searchInput && e.target !== suggestionsContainer) {
      suggestionsContainer.style.display = 'none';
    }
  });
}

// Select a station and show its connections
function selectStation(stationName) {
  // Reset previous selection
  resetSelection();
  
  // Set new selected station
  selectedStation = stationName;
  document.getElementById('selected-station').textContent = stationName;
  
  // Find the station object
  const station = stations.find(s => s.name === stationName);
  
  if (station) {
    // Center map on selected station
    map.setView([station.latitude, station.longitude], 6);
    
    // Highlight the selected station marker
    if (markers[stationName]) {
      markers[stationName].getElement().classList.add('selected-station');
    }
    
    // Show connections
    showConnectionsForStation(stationName);
  }
}

// Show connections for the selected station
function showConnectionsForStation(stationName) {
  const stationConnections = connections[stationName] || [];
  const connectionsListElement = document.getElementById('connections-list');
  
  // Clear previous connections
  connectionsListElement.innerHTML = '';
  
  if (stationConnections.length === 0) {
    connectionsListElement.innerHTML = '<p>No direct connections found for this station.</p>';
  } else {
    // Add each connection to the list
    stationConnections.forEach(connection => {
      const connectionItem = document.createElement('div');
      connectionItem.classList.add('connection-item');
      
      connectionItem.innerHTML = `
        <p><strong>${connection.name}</strong></p>
        <p><small>Operator: ${connection.operator}</small></p>
      `;
      
      // Add click event to focus on the connection
      connectionItem.addEventListener('click', () => {
        // Draw the route line
        drawRouteLine(stationName, connection);
        
        // Zoom the map to show the connection
        const bounds = L.latLngBounds(
          [stations.find(s => s.name === stationName).latitude, 
           stations.find(s => s.name === stationName).longitude],
          [connection.latitude, connection.longitude]
        );
        map.fitBounds(bounds, { padding: [50, 50] });
      });
      
      connectionsListElement.appendChild(connectionItem);
      
      // Draw the route line on the map
      drawRouteLine(stationName, connection);
    });
  }
  
  // Show the connections panel
  document.getElementById('connection-results').style.display = 'block';
}

// Draw a route line between two stations
function drawRouteLine(originName, destination) {
  const originStation = stations.find(s => s.name === originName);
  
  if (!originStation) return;
  
  // Get color based on operator
  const color = operatorColors[destination.operator] || operatorColors.default;
  
  // Create the line
  const routeLine = L.polyline(
    [
      [originStation.latitude, originStation.longitude],
      [destination.latitude, destination.longitude]
    ],
    {
      color: color,
      weight: 3,
      opacity: 0.7
    }
  ).addTo(map);
  
  // Add tooltip
  routeLine.bindTooltip(`${originName} → ${destination.name}<br>Operator: ${destination.operator}`);
  
  // Store the line reference for later removal
  routeLines.push(routeLine);
}

// Reset the current selection
function resetSelection() {
  // Clear route lines
  routeLines.forEach(line => map.removeLayer(line));
  routeLines = [];
  
  // Reset station markers
  Object.keys(markers).forEach(stationName => {
    if (markers[stationName].getElement()) {
      markers[stationName].getElement().classList.remove('selected-station');
    }
  });
}

// Setup event listeners
function setupEventListeners() {
  // Add station marker CSS
  addCustomCSS();
  
  // Add resize handler for the map
  window.addEventListener('resize', () => {
    map.invalidateSize();
  });
}

// Add custom CSS for map elements
function addCustomCSS() {
  const style = document.createElement('style');
  style.textContent = `
    .station-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background-color: #555;
      border: 2px solid white;
      box-shadow: 0 0 2px rgba(0,0,0,0.3);
    }
    .selected-station .station-dot {
      width: 12px;
      height: 12px;
      background-color: #ff5722;
      border: 3px solid white;
      box-shadow: 0 0 4px rgba(0,0,0,0.5);
    }
  `;
  document.head.appendChild(style);
}