import uuid

import sqlalchemy as sa

from src.core.database.db import Base


class File(Base):

    __tablename__ = "files"

    uuid = sa.Column(sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = sa.Column(sa.String, nullable=False)
    path = sa.Column(sa.String, nullable=False)
    owner = sa.Column(sa.ForeignKey("users.uuid"), nullable=True)
