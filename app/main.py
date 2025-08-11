import logging

from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI

from app.config import settings
from app.constants import BASE_STATICS_DIR
from app.routers import berries

logging.basicConfig(level=settings.logger_level)

app = FastAPI(
    title="Poké API",
    version="0.1.0",
    docs_url="/",
)

app.mount("/static", StaticFiles(directory=BASE_STATICS_DIR), name="static")

app.include_router(berries.router, tags=["Berry statistics"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
