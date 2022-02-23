from config import Settings, get_settings
from fastapi import APIRouter, Depends

router = APIRouter(
    tags=["status"],
)


@router.get("/")
async def pong(settings: Settings = Depends(get_settings)):
    """
    Return app settings
    """
    return {
        "message": "Hello World",
        "environment": settings.environment,
        "testing": settings.testing,
    }
