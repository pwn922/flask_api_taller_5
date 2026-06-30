import { useCallback, useEffect, useState } from "react";

import { useSensorSocket } from "./useSensorSocket";
import {
  DEFAULT_DEVICE_ID,
  getLatestSensorState,
  getSensorHistory,
  getSensorAverages,
} from "../services/sensorApi";

const DEVICE_ID = DEFAULT_DEVICE_ID;
const HISTORY_LIMIT = 10;
const AVERAGES_HOURS = 24;
const REFRESH_INTERVAL_MS = 10000;
const REALTIME_SERIES_LIMIT = 12;

export function useSensorDashboard() {
  const [latest, setLatest] = useState(null);
  const [lastRealtimeData, setLastRealtimeData] = useState(null);
  const [history, setHistory] = useState([]);
  const [averages, setAverages] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [realtimeSeries, setRealtimeSeries] = useState([]);

  const handleSensorData = useCallback((sensorData) => {
    setLastRealtimeData(sensorData);

    setRealtimeSeries((currentSeries) => {
      const alreadyExists = currentSeries.some(
        (item) => item.id === sensorData.id
      );

      if (alreadyExists) {
        return currentSeries;
      }

      return [...currentSeries, sensorData].slice(-REALTIME_SERIES_LIMIT);
    });
  }, []);

  const { socketStatus, realtimeAlerts } = useSensorSocket({
    onSensorData: handleSensorData,
  });

  const loadSensorData = useCallback(async () => {
    try {
      const [latestResponse, historyResponse, averagesResponse] =
        await Promise.all([
          getLatestSensorState(DEVICE_ID),
          getSensorHistory(DEVICE_ID, HISTORY_LIMIT),
          getSensorAverages(DEVICE_ID, AVERAGES_HOURS),
        ]);

      const historyData = historyResponse.data ?? [];

      setLatest(latestResponse);
      setHistory(historyData);
      setAverages(averagesResponse);
      setError("");

      setRealtimeSeries((currentSeries) => {
        if (currentSeries.length > 0) {
          return currentSeries;
        }

        return [...historyData].reverse().slice(-REALTIME_SERIES_LIMIT);
      });
    } catch (err) {
      setError("No se pudieron cargar los datos del sensor.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      loadSensorData();
    }, 0);

    const intervalId = setInterval(() => {
      loadSensorData();
    }, REFRESH_INTERVAL_MS);

    return () => {
      clearTimeout(timeoutId);
      clearInterval(intervalId);
    };
  }, [loadSensorData]);

  const latestData = lastRealtimeData ?? latest?.data;
  const isOnline = latest?.online === true;

  return {
    latestData,
    history,
    averages,
    loading,
    error,
    isOnline,
    socketStatus,
    realtimeAlerts,
    realtimeSeries,
  };
}