import logging

from app import config

logger = logging.getLogger(__name__)


class EvaluateAlertsUseCase:
    def execute(
        self,
        temperature: float,
        water_level: float,
    ) -> list[dict]:
        alerts: list[dict] = []
        cfg = config.ActiveConfig

        if temperature > cfg.ALERT_TEMP_MAX:
            alerts.append({
                "type": "alert",
                "severity": "danger",
                "kind": "high_temperature",
                "message": f"Temperatura {temperature}°C supera el límite ({cfg.ALERT_TEMP_MAX}°C)",
                "value": temperature,
                "threshold": cfg.ALERT_TEMP_MAX,
            })
            logger.warning(
                "ALERT: high_temperature | %.1f°C > %.1f°C",
                temperature,
                cfg.ALERT_TEMP_MAX,
            )

        if water_level < cfg.ALERT_WATER_MIN:
            alerts.append({
                "type": "alert",
                "severity": "warning",
                "kind": "low_water",
                "message": f"Nivel de agua {water_level}% está por debajo del mínimo ({cfg.ALERT_WATER_MIN}%)",
                "value": water_level,
                "threshold": cfg.ALERT_WATER_MIN,
            })
            logger.warning(
                "ALERT: low_water | %.1f%% < %.1f%%",
                water_level,
                cfg.ALERT_WATER_MIN,
            )

        return alerts
