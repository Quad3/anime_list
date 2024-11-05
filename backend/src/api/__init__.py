from fastapi import APIRouter

from anime.router import router as anime_router
from auth.router import router as auth_router
from config import settings


router = APIRouter(prefix=settings.API_V1_STR)

router.include_router(auth_router)
router.include_router(anime_router)
