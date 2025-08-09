from fastapi import FastAPI

from .routers import berries


app = FastAPI(
    title="Poké API",
    version="0.1.0",
)

app.include_router(berries.router)
