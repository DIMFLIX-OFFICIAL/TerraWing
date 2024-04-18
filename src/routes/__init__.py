from typing import Final
from fastapi.routing import APIRouter

from .broadcast import router as broadcast_router

main_router: Final[APIRouter] = APIRouter()
main_router.include_router(broadcast_router)
