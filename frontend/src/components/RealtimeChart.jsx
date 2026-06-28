export function RealtimeChart({ data }) {
  const points = data.slice(-12);

  if (points.length < 2) {
    return (
      <article className="panel chart-panel">
        <div className="chart-header">
          <div>
            <h2>Gráfico en tiempo real</h2>
            <p>Esperando más datos del sensor para dibujar la tendencia.</p>
          </div>
        </div>
      </article>
    );
  }

  const width = 720;
  const height = 260;
  const padding = 36;

  const temperatures = points.map((item) => Number(item.temperature));
  const minTemp = Math.min(...temperatures);
  const maxTemp = Math.max(...temperatures);
  const range = maxTemp - minTemp || 1;

  const chartWidth = width - padding * 2;
  const chartHeight = height - padding * 2;

  const path = points
    .map((item, index) => {
      const x =
        padding + (index / Math.max(points.length - 1, 1)) * chartWidth;

      const y =
        height -
        padding -
        ((Number(item.temperature) - minTemp) / range) * chartHeight;

      return `${index === 0 ? "M" : "L"} ${x} ${y}`;
    })
    .join(" ");

  const lastPoint = points[points.length - 1];

  return (
    <article className="panel chart-panel">
      <div className="chart-header">
        <div>
          <h2>Gráfico en tiempo real</h2>
          <p>Últimas temperaturas recibidas por WebSocket.</p>
        </div>

        <strong>{lastPoint.temperature} °C</strong>
      </div>

      <svg
        className="chart"
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label="Gráfico de temperatura en tiempo real"
      >
        <line
          x1={padding}
          y1={padding}
          x2={padding}
          y2={height - padding}
          className="chart-axis"
        />
        <line
          x1={padding}
          y1={height - padding}
          x2={width - padding}
          y2={height - padding}
          className="chart-axis"
        />

        <text x={padding} y={padding - 10} className="chart-label">
          {maxTemp.toFixed(1)} °C
        </text>

        <text x={padding} y={height - 8} className="chart-label">
          {minTemp.toFixed(1)} °C
        </text>

        <path d={path} className="chart-line" />

        {points.map((item, index) => {
          const x =
            padding + (index / Math.max(points.length - 1, 1)) * chartWidth;

          const y =
            height -
            padding -
            ((Number(item.temperature) - minTemp) / range) * chartHeight;

          return (
            <circle
              key={item.id ?? `${item.timestamp}-${index}`}
              cx={x}
              cy={y}
              r="5"
              className="chart-point"
            />
          );
        })}
      </svg>
    </article>
  );
}