import { useEffect, useState } from "react";

const WS_URL =
  import.meta.env.VITE_WS_URL ?? "ws://localhost:8000/sensor-data";

export function useSensorSocket({ onSensorData } = {}) {
  const [socketStatus, setSocketStatus] = useState("disconnected");
  const [realtimeAlerts, setRealtimeAlerts] = useState([]);

  useEffect(() => {
    const socket = new WebSocket(WS_URL);

    socket.onopen = () => {
      setSocketStatus("connected");
    };

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);

      if (message.type === "alert") {
        setRealtimeAlerts((currentAlerts) =>
          [message, ...currentAlerts].slice(0, 5)
        );
        return;
      }

      if (message.device_id) {
        onSensorData?.(message);
      }
    };

    socket.onerror = () => {
      setSocketStatus("error");
    };

    socket.onclose = () => {
      setSocketStatus("disconnected");
    };

    return () => {
      socket.close();
    };
  }, [onSensorData]);

  return {
    socketStatus,
    realtimeAlerts,
  };
}