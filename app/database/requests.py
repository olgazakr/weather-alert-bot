from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select


async def set_user(telegram_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.telegram_id == telegram_id)
        )
    
        if not user:
            session.add(User(telegram_id=telegram_id))
            await session.commit()


async def set_coordinates_for_user(telegram_id: int,
                                   latitude: float,
                                   longitude: float) -> None:
    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.telegram_id == telegram_id)
        )
        user.latitude = latitude
        user.longitude = longitude
        await session.commit()