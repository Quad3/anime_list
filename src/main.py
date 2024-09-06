import uvicorn
from fastapi import FastAPI

from api import router as api_router


app = FastAPI(
    title="My Anime List"
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
