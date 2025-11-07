from fastapi import APIRouter, Depends, File as FileField
from fastapi import UploadFile

from src.core.database.models import User
from src.dependencies.auth import get_current_user
from src.jobs import job_manager

router = APIRouter(prefix="/file", tags=["File"])

@router.post("/upload")
async def upload(upload_file: UploadFile = FileField(...), user: User = Depends(get_current_user)):
    data: bytes = await upload_file.read()
    job = await job_manager.create_job(data)
    return {"job_id": job.uuid, "status": job.status}
