const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

const DEFAULT_DEVICE_ID = import.meta.env.VITE_DEFAULT_DEVICE_ID ?? "esp32_1";

function buildApiUrl(path) {
  return `${API_BASE_URL.replace(/\/$/, "")}${path}`;
}

async function request(path) {
  const response = await fetch(buildApiUrl(path));

  if (!response.ok) {
    throw new Error(`Error HTTP ${response.status}`);
  }

  return response.json();
}

export function getDevices() {
  return request("/api/sensor/devices");
}

export function getLatestSensorState(deviceId = DEFAULT_DEVICE_ID) {
  return request(`/api/sensor/${deviceId}/latest`);
}

export function getSensorHistory(deviceId = DEFAULT_DEVICE_ID, limit = 10) {
  return request(`/api/sensor/${deviceId}/history?limit=${limit}`);
}

export function getSensorAverages(deviceId = DEFAULT_DEVICE_ID, hours = 24) {
  return request(`/api/sensor/${deviceId}/averages?hours=${hours}`);
}

export { DEFAULT_DEVICE_ID };
