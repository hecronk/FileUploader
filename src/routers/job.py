from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database.db import get_db
from src.core.database.models import User
from src.core.database.models.job import Job
from src.dependencies.auth import get_current_user


router = APIRouter(prefix="/jobs", tags=["File"])


@router.get("/{job}")
async def check(job: str = "", db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    job_uuid = job

    if not job_uuid:
        return {
            "message": "Failed to find such job"
        }

    status = db.query(Job).filter_by(uuid=job_uuid).first().status

    return {
        "job": job_uuid,
        "status": status
    }
