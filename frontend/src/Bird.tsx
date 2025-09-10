import { useEffect, useState } from "react"
import { useParams } from "react-router-dom";
import MapComponent from "./components/MapComponent";
import './Bird.css';

const backendURL = import.meta.env.VITE_BACKEND_URL

interface Bird {
    species: string;
    const: number;
    lat: number;
    long: number;
    temp: number;
    percipitation: number;
    wind_speed: number;
    solar_insolation: number;
    clearness_index: number;
    relative_humidity: number;
    pressure: number;
}

interface Coordinates {
    lat: number;
    lng: number;
}

const Bird = () => {
    const { id } = useParams()
    const [coordinates, setCoordinates] = useState<Coordinates | null>(null);
    const [prediction, setPrediction] = useState("")
    const [bird, setBird] = useState<Bird | null>(null)
    const [isLoading, setIsLoading] = useState(false)

    const handlePredict = async () => {
        setIsLoading(true)
        fetch(`${backendURL}/birds/prediction`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                lat: coordinates?.lat,
                long: coordinates?.lng,
                temp: bird?.temp,
                percipitation: bird?.percipitation,
                wind_speed: bird?.wind_speed,
                solar_insolation: bird?.solar_insolation,
                clearness_index: bird?.clearness_index,
                relative_humidity: bird?.relative_humidity,
                pressure: bird?.pressure,
                const: bird?.const,
                latWeight: bird?.lat,
                lngWeight: bird?.long,
                expected: 15
            })
        })
            .then(response => response.json())
            .then(data => {
                console.log("Response from Flask:", data);
                setPrediction(data.fallback_value);
                setIsLoading(false)
            })
            .catch(err => {
                console.error("Error:", err)
                setIsLoading(false)
            });
    }

    useEffect(() => {
        const fetchBird = async () => {
            const response = await fetch(`${backendURL}/birds/weights/${id}`)
            const data = await response.json();
            if (data) {
                console.log(data)
                setBird(data)
            }
        }
        fetchBird();
    }, [])

    return (
        <div className="bird-page">
            <div className="hero-section">
                <div className="hero-content">
                    <h1 className="hero-title">
                        <span className="hero-icon">🦅</span>
                        Bird Prediction
                    </h1>
                    <p className="hero-subtitle">
                        Select a location and predict bird behavior using advanced ML models
                    </p>
                </div>
            </div>

            <div className="main-content">
                <div className="content-grid">
                    <div className="map-section">
                        <div className="section-header">
                            <h2>Choose Location</h2>
                            <p>Click anywhere on the map to set coordinates</p>
                        </div>
                        <div className="map-wrapper">
                            <MapComponent onCoordinatesChange={setCoordinates} />
                        </div>
                    </div>

                    <div className="prediction-section">
                        <div className="section-header">
                            <h2>Prediction Results</h2>
                            <p>Get AI-powered bird behavior insights</p>
                        </div>

                        <div className="prediction-card">
                            {bird && (
                                <div className="bird-info">
                                    <h3>Species: {bird.species}</h3>
                                </div>
                            )}

                            <button 
                                className={`predict-btn ${isLoading ? 'loading' : ''}`}
                                onClick={handlePredict}
                                disabled={!coordinates || !bird || isLoading}
                            >
                                {isLoading ? (
                                    <>
                                        <span className="loading-spinner"></span>
                                        Analyzing...
                                    </>
                                ) : (
                                    <>
                                        <span className="btn-icon">🔮</span>
                                        Generate Prediction
                                    </>
                                )}
                            </button>

                            {prediction && (
                                <div className="prediction-result">
                                    <div className="result-header">
                                        <span className="result-icon">✨</span>
                                        Prediction Complete
                                    </div>
                                    <div className="result-value">{Math.round(parseFloat(prediction))} {bird?.species}s</div>
                                </div>
                            )}

                            {coordinates && (
                                <div className="coordinates-display">
                                    <div className="coord-item">
                                        <span className="coord-label">Latitude</span>
                                        <span className="coord-value">{coordinates.lat.toFixed(6)}</span>
                                    </div>
                                    <div className="coord-item">
                                        <span className="coord-label">Longitude</span>
                                        <span className="coord-value">{coordinates.lng.toFixed(6)}</span>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Bird