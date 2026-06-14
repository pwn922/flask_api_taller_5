from fastapi import APIRouter

from app.health.application.check_health_use_case import CheckHealthUseCase

router = APIRouter()


@router.get("")
def health_check():
    use_case = CheckHealthUseCase()
    status = use_case.execute()
    return {"status": status}
