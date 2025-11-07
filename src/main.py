from fastapi import FastAPI

from src.routers.auth import router as auth_router
from src.routers.file import router as file_router
from src.routers.job import router as job_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(file_router)
app.include_router(job_router)
