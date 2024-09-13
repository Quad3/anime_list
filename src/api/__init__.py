from fastapi import APIRouter

from anime.router import router as anime_router


router = APIRouter(prefix="/api/v1")

router.include_router(anime_router)
