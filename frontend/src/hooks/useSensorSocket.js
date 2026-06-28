import { useEffect, useState } from "react";

const WS_URL = "ws://localhost:8000/sensor-data";

export function useSensorSocket() {
  const [socketStatus, setSocketStatus] = useState("disconnected");
  const [realtimeData, setRealtimeData] = useState(null);
  const [realtimeAlerts, setRealtimeAlerts] = useState([]);

  useEffect(() => {
    const socket = new WebSocket(WS_URL);

    socket.onopen = () => {
      setSocketStatus("connected");
    };

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);

      if (message.type === "alert") {
        setRealtimeAlerts((currentAlerts) => [message, ...currentAlerts].slice(0, 5));
        return;
      }

      if (message.device_id) {
        setRealtimeData(message);
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
  }, []);

  return {
    socketStatus,
    realtimeData,
    realtimeAlerts,
  };
}