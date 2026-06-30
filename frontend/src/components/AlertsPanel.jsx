const HIGH_TEMPERATURE_LIMIT = 35;
const LOW_WATER_LIMIT = 20;

function buildMeasurementAlerts(latestData) {
  if (!latestData) {
    return [];
  }

  const alerts = [];

  const temperature = Number(latestData.temperature);
  const waterLevel = Number(latestData.water_level);

  if (temperature > HIGH_TEMPERATURE_LIMIT) {
    alerts.push({
      kind: "high_temperature",
      severity: "danger",
      message: `Temperatura ${temperature.toFixed(1)}°C supera el límite (${HIGH_TEMPERATURE_LIMIT.toFixed(1)}°C)`,
    });
  }

  if (waterLevel < LOW_WATER_LIMIT) {
    alerts.push({
      kind: "low_water",
      severity: "warning",
      message: `Nivel de agua ${waterLevel.toFixed(1)}% está por debajo del mínimo (${LOW_WATER_LIMIT.toFixed(1)}%)`,
    });
  }

  return alerts;
}

function getPanelStatusClass(alerts) {
  if (alerts.some((alert) => alert.severity === "danger")) {
    return "danger";
  }

  if (alerts.some((alert) => alert.severity === "warning")) {
    return "warning";
  }

  return "success";
}

export function AlertsPanel({ latestData }) {
  const activeAlerts = buildMeasurementAlerts(latestData);

  if (!latestData) {
    return (
      <section className="alerts neutral">
        <h2>Estado de mediciones en tiempo real</h2>

        <article className="alert-status neutral">
          <strong>Esperando mediciones</strong>
          <span>Aún no se han recibido datos recientes del sensor.</span>
        </article>
      </section>
    );
  }

  if (activeAlerts.length === 0) {
    return (
      <section className="alerts success">
        <h2>Estado de mediciones en tiempo real</h2>

        <article className="alert-status success">
          <strong>Mediciones en estado óptimo</strong>
          <span>
            Temperatura, humedad y nivel de agua se encuentran dentro de los
            rangos esperados.
          </span>
        </article>
      </section>
    );
  }

  return (
    <section className={`alerts ${getPanelStatusClass(activeAlerts)}`}>
      <h2>Alertas en tiempo real</h2>

      {activeAlerts.map((alert) => (
        <article
          key={alert.kind}
          className={`alert ${alert.severity}`}
        >
          <strong>{alert.kind}</strong>
          <span>{alert.message}</span>
        </article>
      ))}
    </section>
  );
}