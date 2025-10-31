import React, { useState } from "react";
import "./App.css";
import { MapPin, Truck, Timer, Navigation } from "lucide-react";
import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Custom icon for markers
const markerIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

function App() {
  const [current, setCurrent] = useState("");
  const [pickup, setPickup] = useState("");
  const [dropoff, setDropoff] = useState("");
  const [cycleHours, setCycleHours] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // 👇 Use environment variable (configured in .env)
  const API_URL = process.env.REACT_APP_API_URL;

  const computeRoute = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/trips/compute-route/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          current_location: current,
          pickup_location: pickup,
          dropoff_location: dropoff,
          cycle_hours: cycleHours || 0,
        }),
      });

      const data = await response.json();
      setLoading(false);

      if (!response.ok) {
        console.error("Server error:", data);
        setError(data.error || "Failed to compute route");
        return;
      }

      setResult(data);
    } catch (err) {
      console.error("Fetch error:", err);
      setError("Error connecting to server. Please check your network or backend status.");
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="card">
        <h1 className="title">
          <Truck className="icon" size={28} /> ELD Route & Cycle Calculator
        </h1>

        <form onSubmit={computeRoute} className="form">
          <div className="input-group">
            <MapPin className="input-icon" size={18} />
            <input
              type="text"
              value={current}
              onChange={(e) => setCurrent(e.target.value)}
              placeholder="Current Location"
              required
            />
          </div>

          <div className="input-group">
            <Navigation className="input-icon" size={18} />
            <input
              type="text"
              value={pickup}
              onChange={(e) => setPickup(e.target.value)}
              placeholder="Pickup Location"
              required
            />
          </div>

          <div className="input-group">
            <Navigation className="input-icon" size={18} />
            <input
              type="text"
              value={dropoff}
              onChange={(e) => setDropoff(e.target.value)}
              placeholder="Dropoff Location"
              required
            />
          </div>

          <div className="input-group">
            <Timer className="input-icon" size={18} />
            <input
              type="number"
              value={cycleHours}
              onChange={(e) => setCycleHours(e.target.value)}
              placeholder="Cycle Hours (optional)"
            />
          </div>

          <button type="submit" className="btn" disabled={loading}>
            {loading ? "⏳ Computing..." : "Compute Route"}
          </button>
        </form>

        {error && <p className="error">{error}</p>}

        {result && (
          <>
            <div className="result">
              <h3>📍 Route Summary</h3>
              <p><strong>Pickup:</strong> {result.pickup}</p>
              <p><strong>Dropoff:</strong> {result.dropoff}</p>
              <p><strong>Distance:</strong> {result.distance_km} km</p>
              <p><strong>Estimated Time:</strong> {result.estimated_hours} hrs</p>
              <p><strong>Remaining Cycle Hours:</strong> {result.remaining_cycle_hours}</p>
            </div>

            <div className="map-container">
              <MapContainer
                center={[0.52, 35.27]}
                zoom={10}
                scrollWheelZoom={true}
                style={{ height: "400px", width: "100%", borderRadius: "12px", marginTop: "15px" }}
              >
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
                />
                <Marker position={[0.52, 35.27]} icon={markerIcon}>
                  <Popup>Pickup Location</Popup>
                </Marker>
                <Marker position={[0.55, 35.3]} icon={markerIcon}>
                  <Popup>Dropoff Location</Popup>
                </Marker>
                <Polyline positions={[[0.52, 35.27], [0.55, 35.3]]} color="blue" weight={4} />
              </MapContainer>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
