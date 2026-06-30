const CHILE_TIMEZONE = "America/Santiago";
const CHILE_LOCALE = "es-CL";

function normalizeTimestamp(timestamp) {
  if (!timestamp) {
    return null;
  }

  if (timestamp instanceof Date) {
    return timestamp;
  }

  const timestampText = String(timestamp);

  const hasTimezone =
    timestampText.endsWith("Z") || /[+-]\d{2}:\d{2}$/.test(timestampText);

  const normalizedTimestamp = hasTimezone
    ? timestampText
    : `${timestampText}Z`;

  const date = new Date(normalizedTimestamp);

  if (Number.isNaN(date.getTime())) {
    return null;
  }

  return date;
}

export function formatDateTime(timestamp) {
  const date = normalizeTimestamp(timestamp);

  if (!date) {
    return "--";
  }

  return new Intl.DateTimeFormat(CHILE_LOCALE, {
    timeZone: CHILE_TIMEZONE,
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(date);
}

export function formatTime(timestamp) {
  const date = normalizeTimestamp(timestamp);

  if (!date) {
    return "--";
  }

  return new Intl.DateTimeFormat(CHILE_LOCALE, {
    timeZone: CHILE_TIMEZONE,
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(date);
}