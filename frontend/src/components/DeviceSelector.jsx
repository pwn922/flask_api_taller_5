export function DeviceSelector({ devices, selectedDevice, onSelect }) {
  return (
    <div className="device-selector">
      <label htmlFor="device-select">Dispositivo:</label>
      <select
        id="device-select"
        value={selectedDevice}
        onChange={(e) => onSelect(e.target.value)}
      >
        {devices.map((device) => (
          <option key={device.device_id} value={device.device_id}>
            {device.device_id}
          </option>
        ))}
      </select>
    </div>
  );
}
