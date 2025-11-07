import uuid

import sqlalchemy as sa

from src.core.database.db import Base


class Job(Base):

    __tablename__ = "jobs"

    uuid = sa.Column(sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = sa.Column(sa.Enum("pending", "processing", "completed", "failed", name="status"), default="pending")
