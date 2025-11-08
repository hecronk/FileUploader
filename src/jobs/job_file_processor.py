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
    app: Annotated[Any]

    @staticmethod
    def check_for_virus(path: str):
        time.sleep(10)
        return "OK"

    def process_file_job(self):
        time.sleep(15)
        loop = self.app.state.loop
        self.job.status = "processing"
        asyncio.run_coroutine_threadsafe(self.job.broadcast_progress(), loop)

        media_path = pathlib.Path(settings.media_path)
        file_path = media_path.joinpath(self.file.filename)
        if not media_path.exists():
            self.job.status = "failed"
            future_ws = asyncio.run_coroutine_threadsafe(self.job.broadcast_progress(), loop)
            future_ws.result()
        else:
            with open(file_path, mode="wb") as f:
                f.write(self.job.data)
            self.job.status = "checking for viruses"
            future_ws = asyncio.run_coroutine_threadsafe(self.job.broadcast_progress(), loop)
            future_ws.result()
            future = self.app.state.process_pool.submit(JobFileProcessor.check_for_virus, str(file_path))
            result = future.result()
            if result == "OK":
                self.job.status = "completed"
            else:
                self.job.status = "failed"
            future_ws = asyncio.run_coroutine_threadsafe(self.job.broadcast_progress(), loop)
            future_ws.result()
