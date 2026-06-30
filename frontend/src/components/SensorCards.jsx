import { formatDateTime } from "../utils/dateFormat";

export function SensorCards({ latestData }) {
  return (
    <section className="cards">
      <article className="card">
        <span>Temperatura</span>
        <strong>{latestData ? `${latestData.temperature} °C` : "--"}</strong>
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
        <strong className="small">{formatDateTime(latestData?.timestamp)}</strong>
      </article>
    </section>
  );
}