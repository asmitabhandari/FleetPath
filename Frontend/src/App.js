import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Polyline } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './App.css';

function App() {
  const [locations, setLocations] = useState([]);
  const [optimizedRoute, setOptimizedRoute] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showRoute, setShowRoute] = useState(false);

  const mapCenter = [42.4950, -83.3640];
  const mapZoom = 13;

  // Fetch initial locations
  useEffect(() => {
    fetchLocations();
  }, []);

  const fetchLocations = async () => {
    try {
      const response = await fetch('http://localhost:8000/locations');
      const data = await response.json();
      setLocations(data);
    } catch (error) {
      console.error('Error fetching locations:', error);
    }
  };

  const optimizeRoute = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/optimize');
      const data = await response.json();
      setOptimizedRoute(data.route);
      setMetrics(data.metrics);
      setShowRoute(true);
    } catch (error) {
      console.error('Error optimizing route:', error);
    } finally {
      setLoading(false);
    }
  };

  const resetRoute = () => {
    setShowRoute(false);
    setOptimizedRoute([]);
    setMetrics(null);
  };

  const routePositions = optimizedRoute.map(loc => [Number(loc.lat), Number(loc.lon)]);
  const visibleLocations = showRoute ? optimizedRoute : locations;

  const createMarkerIcon = (label, isDepot) => {
    const size = isDepot ? 44 : 36;
    const className = isDepot ? 'marker depot' : 'marker';
    return L.divIcon({
      className: 'marker-wrapper',
      html: `<div class="${className}">${label}</div>`,
      iconSize: [size, size],
      iconAnchor: [size / 2, size / 2]
    });
  };

  return (
    <div className="App">
      <div className="header">
        <h1>🚛 Waste Collection Route Optimizer</h1>
        <p>Optimize your waste collection routes to save fuel and time</p>
      </div>

      <div className="container">
        <div className="sidebar">
          <div className="control-panel">
            <h2>Route Control</h2>
            
            <button 
              onClick={optimizeRoute} 
              disabled={loading}
              className="btn btn-primary"
            >
              {loading ? 'Optimizing...' : '⚡ Optimize Route'}
            </button>

            {showRoute && (
              <button 
                onClick={resetRoute}
                className="btn btn-secondary"
              >
                🔄 Reset
              </button>
            )}
          </div>

          {metrics && (
            <div className="metrics-panel">
              <h2>Route Metrics</h2>
              
              <div className="metric-card">
                <div className="metric-label">Total Stops</div>
                <div className="metric-value">{metrics.total_stops}</div>
              </div>

              <div className="metric-card">
                <div className="metric-label">Original Route</div>
                <div className="metric-value">{metrics.original_miles} mi</div>
              </div>

              <div className="metric-card highlight">
                <div className="metric-label">Optimized Route</div>
                <div className="metric-value">{metrics.optimized_miles} mi</div>
              </div>

              <div className="metric-card success">
                <div className="metric-label">Distance Saved</div>
                <div className="metric-value">
                  {metrics.savings_miles} mi ({metrics.savings_percentage}%)
                </div>
              </div>

              <div className="metric-card">
                <div className="metric-label">Est. Fuel Savings</div>
                <div className="metric-value">
                  {metrics.estimated_fuel_savings_gallons} gal
                </div>
              </div>
            </div>
          )}

          <div className="locations-panel">
            <h2>Pickup Locations ({locations.length})</h2>
            <div className="locations-list">
              {(showRoute ? optimizedRoute : locations).map((loc, idx) => (
                <div key={loc.id} className="location-item">
                  <span className="location-number">{showRoute ? idx + 1 : loc.id}</span>
                  <span className="location-name">{loc.address}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="map-container">
          <MapContainer center={mapCenter} zoom={mapZoom} scrollWheelZoom={true}>
            <TileLayer
              attribution='&copy; OpenStreetMap contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {showRoute && routePositions.length > 0 && (
              <Polyline
                key={`route-${routePositions.length}`}
                positions={routePositions}
                pathOptions={{ color: '#3b82f6', weight: 4 }}
              />
            )}

            {visibleLocations.map((location, idx) => (
              <Marker
                key={location.id}
                position={[Number(location.lat), Number(location.lon)]}
                icon={createMarkerIcon(showRoute ? idx + 1 : location.id, idx === 0)}
              />
            ))}
          </MapContainer>
        </div>
      </div>
    </div>
  );
}

export default App;