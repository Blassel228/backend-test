from typing import List, Optional
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, CreatedAtModel


class Product(Base, CreatedAtModel):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    brand_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("brands.id", ondelete="SET NULL"),
        nullable=True,
    )

    image: Mapped[Optional[str]] = mapped_column(Text)

    brand: Mapped[Optional["Brand"]] = relationship(back_populates="products")

    categories: Mapped[List["Category"]] = relationship(
        secondary="product_categories",
        back_populates="products",
    )
