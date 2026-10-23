from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Text, String

class LinksData(Base):
    __tablename__ = "links_data"

    real_link: Mapped[str] = mapped_column(Text, nullable=False)
    hash: Mapped[str] = mapped_column(String(6), nullable=False)