export function AveragesPanel({ averages }) {
  return (
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
  );
}