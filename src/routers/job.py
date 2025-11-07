from fastapi import APIRouter, HTTPException, WebSocket
from starlette.websockets import WebSocketDisconnect

from src.jobs import job_manager


router = APIRouter(prefix="/jobs", tags=["File"])


@router.websocket("/ws/{job_uuid}")
async def get_job_status_ws(websocket: WebSocket, job_uuid: str):
    await websocket.accept()

    job = await job_manager.get_job(job_uuid)

    if not job:
        await websocket.close(code=1000)
        return

    job.websocket_subscribers.add(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        job.websocket_subscribers.remove(websocket)


@router.get("/{job_uuid}")
async def get_job_status(job_uuid: str):
    job = await job_manager.get_job(job_uuid)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.to_dict()


@router.get("/jobs")
async def list_jobs():
    return await job_manager.list_jobs()
