from fastapi import FastAPI

from src.routers.auth import router as auth_router
from src.routers.file import router as file_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(file_router)
