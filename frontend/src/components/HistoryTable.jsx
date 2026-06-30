import { formatTime } from "../utils/dateFormat";

export function HistoryTable({ history }) {
  return (
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
                <td>{formatTime(item.timestamp)}</td>
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
  );
}