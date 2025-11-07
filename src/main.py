from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from fastapi import FastAPI

from src.routers.auth import router as auth_router
from src.routers.file import router as file_router
from src.routers.job import router as job_router

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    app.state.thread_pool = ThreadPoolExecutor(max_workers=10)
    app.state.process_pool = ProcessPoolExecutor(max_workers=4)

@app.on_event("shutdown")
async def shutdown_event():
    app.state.thread_pool.shutdown(wait=True)
    app.state.process_pool.shutdown(wait=True)

app.include_router(auth_router)
app.include_router(file_router)
app.include_router(job_router)
