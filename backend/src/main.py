import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router as api_router
from config import settings


app = FastAPI(
    title="My Anime List",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_HOST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
