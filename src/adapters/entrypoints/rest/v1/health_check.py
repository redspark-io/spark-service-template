from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health-check")
def health_check():
    """
    Health check endpoint
    """
    return JSONResponse({"status": "ok"})
