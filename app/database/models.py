"""
This module defines the database models for the application.
"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import (AsyncAttrs,
                                    create_async_engine,
                                    async_sessionmaker)


# Create an asynchronous engine for the SQLite database
engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

# Create an asynchronous session factory for the database
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for database models.
    """
    pass


class User(Base):
    """
    User model.
    """

    # Table name
    __tablename__ = 'users'

    # Columns
    id: Mapped[int] = mapped_column(
        primary_key=True,  # Primary key
        autoincrement=True  # Auto-incrementing
    )
    telegram_id: Mapped[int] = mapped_column(
        unique=True  # Unique constraint
    )
    telegram_username: Mapped[str] = mapped_column(
        nullable=True  # Allow null values
    )
    latitude: Mapped[float] = mapped_column(
        nullable=True  # Allow null values
    )
    longitude: Mapped[float] = mapped_column(
        nullable=True  # Allow null values
    )
    is_notified: Mapped[bool] = mapped_column(
        default=False  # Set default value to True
    )
    notified_condition: Mapped[str] = mapped_column(
        nullable=True  # Allow null values
    )


async def async_main():
    """
    Create the database tables if they do not exist.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

