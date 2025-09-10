import React, { useState, useCallback } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

interface Coordinates {
  lat: number;
  lng: number;
}
interface MapComponentProps {
  onCoordinatesChange: (coords: Coordinates) => void;
}


const defaultIcon = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

L.Marker.prototype.options.icon = defaultIcon;

interface MapEventsProps {
  onMapClick: (coords: Coordinates) => void;
}

const MapEvents: React.FC<MapEventsProps> = ({ onMapClick }) => {
  const map = useMapEvents({
    click: (e) => {
      const { lat, lng } = e.latlng;
      onMapClick({ lat, lng });
    },
  });

  return null;
};

const MapComponent: React.FC<MapComponentProps> = ({ onCoordinatesChange }) => {

  const [coordinates, setCoordinates] = useState<Coordinates>({
    lat: 37.7749,
    lng: -122.4194
  });

  const onMapClick = useCallback((coords: Coordinates) => {
    setCoordinates(coords);
    onCoordinatesChange(coords); 
  }, []);

  const handleCoordChange = (field: keyof Coordinates, value: string): void => {
    const numValue = parseFloat(value);
    if (!isNaN(numValue)) {
      setCoordinates(prev => ({ ...prev, [field]: numValue }));
    }
  };

  const handleInputChange = (field: keyof Coordinates) => (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    handleCoordChange(field, event.target.value);
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-6 bg-gray-50 p-4 rounded-lg">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Latitude:</label>
            <input
              type="number"
              step="any"
              value={coordinates.lat}
              onChange={handleInputChange('lat')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="37.7749"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Longitude:</label>
            <input
              type="number"
              step="any"
              value={coordinates.lng}
              onChange={handleInputChange('lng')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="-122.4194"
            />
          </div>
        </div>
      </div>

      <div className="mb-6" style={{ height: '400px', width: '45vw', zIndex: 1 }}>
        <MapContainer
          center={[coordinates.lat, coordinates.lng]}
          zoom={10}
          style={{ height: '100%', width: '45vw' }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          
          <MapEvents onMapClick={onMapClick} />
          
          <Marker position={[coordinates.lat, coordinates.lng]} icon={defaultIcon}>
            <Popup>
              Lat: {coordinates.lat.toFixed(6)}<br />
              Lng: {coordinates.lng.toFixed(6)}
            </Popup>
          </Marker>
        </MapContainer>
      </div>

      <div className="bg-blue-50 p-4 rounded-lg">
        <p className="text-sm text-gray-700">
          Latitude: <span className="font-mono">{coordinates.lat.toFixed(6)}</span>
        </p>
        <p className="text-sm text-gray-700">
          Longitude: <span className="font-mono">{coordinates.lng.toFixed(6)}</span>
        </p>
      </div>
    </div>
  );
};

export default MapComponent;