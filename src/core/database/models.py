import sqlalchemy as sa

import uuid

from src.core.database.db import Base


class User(Base):

    __tablename__ = "users"
    __table_args__ = (sa.UniqueConstraint("username"),)

    uuid = sa.Column(sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = sa.Column(sa.String, nullable=False, unique=True)
    hashed_password = sa.Column(sa.String, nullable=False)
