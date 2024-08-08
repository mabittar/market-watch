from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Health Checker"])


@router.get(
    path="/health",
    response_class=JSONResponse,
    name="health-check",
    status_code=status.HTTP_200_OK,
)
async def check_health() -> JSONResponse:
    return JSONResponse(content={"status": "💚"})
