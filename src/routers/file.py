import pathlib
import shutil

from fastapi import APIRouter, Depends, File as FileField
from sqlalchemy.orm import Session
from fastapi import UploadFile

from src.core.database.db import get_db
from src.core.database.models import User, File
from src.core.database.models.job import Job
from src.core.settings.settings import settings
from src.dependencies.auth import get_current_user

router = APIRouter(prefix="/file", tags=["File"])

@router.post("/upload")
async def upload(upload_file: UploadFile = FileField(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    file_path = None

    try:
        job = Job()
        db.add(job)
        db.commit()
    except Exception as e:
        return {"message": "Failed to upload file"}


    try:
        file_path = pathlib.Path(settings.media_path).joinpath(upload_file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(upload_file.file, f)
        job.status = "processing"
    except Exception as e:
        job.status = "failed"
        return {"message": "Failed to upload file"}
    finally:
        db.add(job)
        db.commit()
        db.refresh(job)

    if file_path and file_path.exists():
        file = File(
            filename=upload_file.filename,
            path=str(file_path.resolve()),
            owner=user.uuid
        )
        db.add(file)
        db.commit()
        job.status = "completed"
        db.add(job)
        db.commit()
        db.refresh(job)
        return {"message": "Successfully uploaded file", "job uuid": job.uuid}
    else:
        job.status = "failed"
        db.add(job)
        db.commit()
        return {"message": "Failed to upload file"}
