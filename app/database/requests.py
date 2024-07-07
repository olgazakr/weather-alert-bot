from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select


async def set_user(telegram_id: int) -> None:
    """
    Set user in the database if it doesn't exist.

    :param telegram_id: Telegram ID of the user.
    :type telegram_id: int
    """
    async with async_session() as session:
        # Get user from the database
        user = await session.scalar(
            select(User).where(User.telegram_id == telegram_id)
        )

        # If user doesn't exist, add it to the database
        if not user:
            session.add(User(telegram_id=telegram_id))
            await session.commit()


async def set_coordinates_for_user(telegram_id: int,
                                   latitude: float,
                                   longitude: float) -> None:
    """
    Set coordinates for a user in the database.

    :param telegram_id: Telegram ID of the user.
    :type telegram_id: int
    :param latitude: Latitude of the user's location.
    :type latitude: float
    :param longitude: Longitude of the user's location.
    :type longitude: float
    """
    async with async_session() as session:
        # Get user from the database
        user = await session.scalar(
            select(User).where(User.telegram_id == telegram_id)
        )

        # Set user's coordinates in the database
        user.latitude = latitude
        user.longitude = longitude
        await session.commit()
