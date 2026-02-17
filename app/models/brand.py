from typing import List
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, CreatedAtModel


class Brand(Base, CreatedAtModel):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    products: Mapped[List["Product"]] = relationship(
        back_populates="brand",
        passive_deletes=True,
    )
