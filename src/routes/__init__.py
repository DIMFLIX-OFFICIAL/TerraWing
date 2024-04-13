from typing import Final
from fastapi.routing import APIRouter

from . import connect_drone

main_router: Final[APIRouter] = APIRouter()
main_router.include_router(connect_drone.router)
