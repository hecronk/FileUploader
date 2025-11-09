import asyncio
import io
from unittest.mock import MagicMock, AsyncMock

import pytest
from src.jobs.job_file_processor import JobFileProcessor


@pytest.mark.asyncio
async def test_process_file_job(monkeypatch, tmp_path):
    mock_job = MagicMock()
    mock_job.status = "pending"
    mock_job.data = b"some-data"
    mock_job.broadcast_progress = AsyncMock()

    mock_loop = asyncio.get_event_loop()
    mock_app = MagicMock()
    mock_app.state.loop = mock_loop
    mock_app.state.process_pool = MagicMock()

    mock_future = MagicMock()
    mock_future.result.return_value = "OK"
    mock_app.state.process_pool.submit.return_value = mock_future

    monkeypatch.setattr("pathlib.Path.exists", lambda self: True)

    monkeypatch.setattr("time.sleep", lambda x: None)

    fake_future = MagicMock()
    fake_future.result.return_value = None
    monkeypatch.setattr("asyncio.run_coroutine_threadsafe", lambda coro, loop: fake_future)

    from src.core.settings import settings
    monkeypatch.setattr(settings.settings, "media_path", tmp_path)

    from fastapi import UploadFile
    file = UploadFile(filename="test.txt", file=io.BytesIO(b"dummy"))

    processor = JobFileProcessor(job=mock_job, file=file, app=mock_app)
    processor.process_file_job()

    assert mock_job.status == "completed"

    assert mock_job.broadcast_progress.call_count >= 1
    mock_app.state.process_pool.submit.assert_called_once()
