from fastapi import APIRouter, Depends, File
from fastapi import UploadFile, Request

from src.core.database.models import User
from src.dependencies.auth import get_current_user
from src.jobs import job_manager
from src.jobs.job_file_processor import JobFileProcessor

router = APIRouter(prefix="/file", tags=["File"])

@router.post("/upload")
async def upload(request: Request, upload_file: UploadFile = File(...), user: User = Depends(get_current_user)):
    data: bytes = await upload_file.read()
    job = await job_manager.create_job(data)
    file_processor = JobFileProcessor(job, upload_file, request.app)
    thread_pool = request.app.state.thread_pool
    thread_pool.submit(file_processor.process_file_job)
    return {"job_id": job.uuid, "status": job.status}
