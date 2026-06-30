export function DashboardHeader({ isOnline, socketStatus }) {
  return (
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

        <div
          className={`status ${
            socketStatus === "connected" ? "online" : "offline"
          }`}
        >
          WS: {socketStatus}
        </div>
      </div>
    </section>
  );
}