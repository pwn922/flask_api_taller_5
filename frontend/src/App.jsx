import "./App.css";

import { DashboardHeader } from "./components/DashboardHeader";
import { SensorCards } from "./components/SensorCards";
import { AlertsPanel } from "./components/AlertsPanel";
import { HistoryTable } from "./components/HistoryTable";
import { AveragesPanel } from "./components/AveragesPanel";
import { RealtimeChart } from "./components/RealtimeChart";

import { useSensorDashboard } from "./hooks/useSensorDashboard";

function App() {
  const {
    deviceId,
    devices,
    latestData,
    history,
    averages,
    loading,
    error,
    isOnline,
    socketStatus,
    realtimeAlerts,
    realtimeSeries,
    onDeviceChange,
  } = useSensorDashboard();

  return (
    <main className="dashboard">
      <DashboardHeader
        isOnline={isOnline}
        socketStatus={socketStatus}
        devices={devices}
        selectedDevice={deviceId}
        onDeviceChange={onDeviceChange}
      />

      {loading && <p className="info">Cargando datos...</p>}
      {error && <p className="error">{error}</p>}

      <SensorCards latestData={latestData} />

      <AlertsPanel latestData={latestData} realtimeAlerts={realtimeAlerts} />

      <RealtimeChart data={realtimeSeries} />

      <section className="content-grid">
        <HistoryTable history={history} />
        <AveragesPanel averages={averages} />
      </section>
    </main>
  );
}

export default App;
