import uvicorn
from fastapi import FastAPI

from app.routers import berries

app = FastAPI(
    title="Poké API",
    version="0.1.0",
)

app.include_router(berries.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
