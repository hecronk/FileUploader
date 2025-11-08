import asyncio
import pathlib
import time
from dataclasses import dataclass
from typing import Any

from fastapi import UploadFile
from sqlalchemy.sql.annotation import Annotated

from src.core.settings.settings import settings
from src.jobs.jobs import Job


@dataclass
class JobFileProcessor:
    job: Job
    file: UploadFile
    loop: Annotated[Any]

    def process_file_job(self):
        time.sleep(15)
        self.job.status = "processing"
        asyncio.run_coroutine_threadsafe(self.job.broadcast_progress(), self.loop)

        media_path = pathlib.Path(settings.media_path)
        if not media_path.exists():
            self.job.status = "failed"
            asyncio.run_coroutine_threadsafe(self.job.broadcast_progress(), self.loop)
        else:
            with open(media_path.joinpath(self.file.filename), mode="wb") as f:
                f.write(self.job.data)
            self.job.status = "completed"
            asyncio.run_coroutine_threadsafe(self.job.broadcast_progress(), self.loop)
