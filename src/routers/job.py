from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from src.jobs import job_manager


router = APIRouter(prefix="/jobs", tags=["File"])


@router.get("/{job_uuid}")
async def get_job_status(job_uuid: str):
    job = await job_manager.get_job(job_uuid)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JSONResponse(content=job.to_dict())


@router.get("/jobs")
async def list_jobs():
    return await job_manager.list_jobs()
