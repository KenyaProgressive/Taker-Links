from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import UUID as SA_UUID, TIMESTAMP
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import func

class Base(DeclarativeBase):

    id: Mapped[UUID] = mapped_column(
        SA_UUID(as_uuid=True), primary_key=True, default=uuid4, init=False
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), init=False
    )

