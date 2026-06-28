import { useEffect, useState } from "react";
import { useSensorSocket } from "./hooks/useSensorSocket";
import { RealtimeChart } from "./components/RealtimeChart";
import "./App.css";
import {
  getLatestSensorState,
  getSensorHistory,
  getSensorAverages,
} from "./services/sensorApi";

const DEVICE_ID = "esp32_1";

function App() {
  const [latest, setLatest] = useState(null);
  const [history, setHistory] = useState([]);
  const [averages, setAverages] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { socketStatus, realtimeData, realtimeAlerts } = useSensorSocket();
  const [realtimeSeries, setRealtimeSeries] = useState([]);

  async function loadSensorData() {
    try {
      setError("");

      const [latestResponse, historyResponse, averagesResponse] =
        await Promise.all([
          getLatestSensorState(DEVICE_ID),
          getSensorHistory(DEVICE_ID, 10),
          getSensorAverages(DEVICE_ID, 24),
        ]);

      setLatest(latestResponse);
      setHistory(historyResponse.data ?? []);
      setRealtimeSeries((currentSeries) => {
  if (currentSeries.length > 0) {
    return currentSeries;
  }

  return [...(historyResponse.data ?? [])].reverse().slice(-12);
});
      setAverages(averagesResponse);
    } catch (err) {
      setError("No se pudieron cargar los datos del sensor.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadSensorData();

    const intervalId = setInterval(() => {
      loadSensorData();
    }, 10000);

    return () => clearInterval(intervalId);
  }, []);

  const latestData = realtimeData ?? latest?.data;
  useEffect(() => {
  if (!realtimeData) {
    return;
  }

  setRealtimeSeries((currentSeries) => {
    const alreadyExists = currentSeries.some(
      (item) => item.id === realtimeData.id
    );

    if (alreadyExists) {
      return currentSeries;
    }

    return [...currentSeries, realtimeData].slice(-12);
  });
}, [realtimeData]);
  const isOnline = latest?.online === true;

  return (
    <main className="dashboard">
      <section className="hero">
        <div>
          <p className="eyebrow">Taller 5 - Conexión IoT</p>
          <h1>Dashboard ESP32</h1>
          <p className="description">
            Visualización de datos de sensores usando FastAPI, MongoDB y Redis.
          </p>
        </div>

<div className="status-group">
  <div className={`status ${isOnline ? "online" : "offline"}`}>
    {isOnline ? "Sensor online" : "Sensor sin datos recientes"}
  </div>

  <div className={`status ${socketStatus === "connected" ? "online" : "offline"}`}>
    WS: {socketStatus}
  </div>
</div>
      </section>

      {loading && <p className="info">Cargando datos...</p>}

      {error && <p className="error">{error}</p>}

      <section className="cards">
        <article className="card">
          <span>Temperatura</span>
          <strong>
            {latestData ? `${latestData.temperature} °C` : "--"}
          </strong>
        </article>

        <article className="card">
          <span>Humedad</span>
          <strong>{latestData ? `${latestData.humidity} %` : "--"}</strong>
        </article>

        <article className="card">
          <span>Nivel de agua</span>
          <strong>{latestData ? latestData.water_level : "--"}</strong>
        </article>

        <article className="card">
          <span>Último registro</span>
          <strong className="small">
            {latestData?.timestamp
              ? new Date(latestData.timestamp).toLocaleString()
              : "--"}
          </strong>
        </article>
      </section>
      <RealtimeChart data={realtimeSeries} />
      {realtimeAlerts.length > 0 && (
  <section className="alerts">
    <h2>Alertas en tiempo real</h2>

    {realtimeAlerts.map((alert, index) => (
      <article key={`${alert.kind}-${index}`} className={`alert ${alert.severity}`}>
        <strong>{alert.kind}</strong>
        <span>{alert.message}</span>
      </article>
    ))}
  </section>
)}

      <section className="content-grid">
        <article className="panel">
          <h2>Últimos 10 datos</h2>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Hora</th>
                  <th>Temp.</th>
                  <th>Humedad</th>
                  <th>Agua</th>
                </tr>
              </thead>
              <tbody>
                {history.map((item) => (
                  <tr key={item.id}>
                    <td>{new Date(item.timestamp).toLocaleTimeString()}</td>
                    <td>{item.temperature} °C</td>
                    <td>{item.humidity} %</td>
                    <td>{item.water_level}</td>
                  </tr>
                ))}

                {history.length === 0 && (
                  <tr>
                    <td colSpan="4">Sin datos históricos.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </article>

        <article className="panel">
          <h2>Promedios últimas 24 horas</h2>

          <div className="averages">
            <p>
              <span>Temperatura promedio</span>
              <strong>
                {averages?.avg_temperature
                  ? `${averages.avg_temperature.toFixed(2)} °C`
                  : "--"}
              </strong>
            </p>

            <p>
              <span>Humedad promedio</span>
              <strong>
                {averages?.avg_humidity
                  ? `${averages.avg_humidity.toFixed(2)} %`
                  : "--"}
              </strong>
            </p>

            <p>
              <span>Nivel de agua promedio</span>
              <strong>
                {averages?.avg_water_level
                  ? averages.avg_water_level.toFixed(2)
                  : "--"}
              </strong>
            </p>

            <p>
              <span>Muestras</span>
              <strong>{averages?.samples ?? 0}</strong>
            </p>
          </div>
        </article>
      </section>
    </main>
  );
}

export default App;