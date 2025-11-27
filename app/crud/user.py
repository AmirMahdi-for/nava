from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.auth.jwt import hash_password


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, username: str, password: str):
    user = User(
        username=username,
        password=hash_password(password),
        is_active=1
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
