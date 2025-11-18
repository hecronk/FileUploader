import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set

from starlette.websockets import WebSocket


@dataclass
class Job:
    uuid: str
    data: memoryview
    _status: str = field(default="pending", init=False, repr=False)
    _progress: int = field(default=0, init=False, repr=False)
    initiator: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    websocket_subscribers: Set[WebSocket] = field(default_factory=set)
    error: Optional[str] = None
    result: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "uuid": self.uuid,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "progress": self.progress,
            "error": self.error,
            "result": self.result,
        }

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        if type(value) is int:
            self._progress = value
        else:
            raise ValueError("progress count must be int instance")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value in ("pending", "processing", "checking for viruses", "completed", "failed"):
            self._status = value
        else:
            raise ValueError("status must be one of available statuses")

    async def broadcast_progress(self):
        dead_subs = list()

        for ws in self.websocket_subscribers:
            try:
                await ws.send_json(self.to_dict())
            except Exception as e:
                dead_subs.append(ws)
        for ws in dead_subs:
            self.websocket_subscribers.remove(ws)


class JobManager:
    def __init__(self):
        self.jobs: dict[str, Job] = {}
        self.lock = asyncio.Lock()

    async def create_job(self, data: bytes, initiator) -> Job:
        job_uuid = str(uuid.uuid4())
        job = Job(uuid=job_uuid, data=memoryview(data), initiator=initiator)
        async with self.lock:
            self.jobs[job_uuid] = job
        return job

    async def get_job(self, job_uuid: str) -> Job:
        async with self.lock:
            return self.jobs.get(job_uuid)

    async def list_jobs(self) -> list[dict]:
        async with self.lock:
            return [job.to_dict() for job in self.jobs.values()]
