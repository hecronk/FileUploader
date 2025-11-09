import io
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.dependencies import auth


@pytest.mark.asyncio
async def test_file_upload_with_websocket(monkeypatch):
    mock_job = MagicMock(uuid="1c9a03cf-b862-4116-8b71-d7563c2b5ca4", status="pending")
    mock_job.broadcast_progress = AsyncMock()
    mock_job_manager = AsyncMock()
    mock_job_manager.create_job.return_value = mock_job
    monkeypatch.setattr("src.routers.file.job_manager", mock_job_manager)

    mock_processor = MagicMock()
    monkeypatch.setattr("src.jobs.job_file_processor.JobFileProcessor", MagicMock(return_value=mock_processor))

    fake_thread_pool = MagicMock()
    app.state.thread_pool = fake_thread_pool

    async def fake_get_user():
        return MagicMock(id=1, username="tester")

    app.dependency_overrides[auth.get_current_user] = fake_get_user

    file_content = b"hello world"
    file = io.BytesIO(file_content)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/file/upload",
            files={"upload_file": ("test.txt", file, "text/plain")},
        )

    assert response.status_code == 201
    data = response.json()
    assert data["job_id"] == "1c9a03cf-b862-4116-8b71-d7563c2b5ca4"
    assert data["status"] == "pending"

    fake_thread_pool.submit.assert_called_once()
    mock_job_manager.create_job.assert_awaited_once()

    app.dependency_overrides = {}
