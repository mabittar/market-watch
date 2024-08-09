from fastapi import APIRouter

from .api_health import router as api_health_router
from .stock import router as stock_router

router = APIRouter()

router.include_router(router=api_health_router)
router.include_router(router=stock_router)
