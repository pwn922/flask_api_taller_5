from app.health.domain.health import HealthCheck


class CheckHealthUseCase:
    def execute(self) -> str:
        health_check = HealthCheck()
        return health_check.status()
