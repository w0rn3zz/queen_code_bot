from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from dao import UserDao


class UserService:
    @classmethod
    async def get_user(cls, session: AsyncSession, tg_id: int) -> User | None:
        return await UserDao.find_by_tg_id(session, tg_id)
    
    @classmethod
    async def create_user(
        cls,
        session: AsyncSession,
        tg_id: int,
        username: str | None,
        first_name: str,
        last_name: str | None = None
    ) -> User:
        user_data = {
            "tg_id": tg_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name
        }
        return await UserDao.create(session, user_data)
    
    @classmethod
    async def update_user(
        cls,
        session: AsyncSession,
        tg_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None
    ) -> User | None:
        user = await cls.get_user(session, tg_id)
        if not user:
            return None
        
        if username is not None:
            user.username = username
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        
        await session.commit()
        await session.refresh(user)
        return user
    
    @classmethod
    async def upsert_user(
        cls,
        session: AsyncSession,
        tg_id: int,
        username: str | None,
        first_name: str,
        last_name: str | None = None
    ) -> User:
        user = await cls.get_user(session, tg_id)
        
        if user:
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            await session.commit()
            await session.refresh(user)
        else:
            user = await cls.create_user(
                session, tg_id, username, first_name, last_name
            )
        
        return user
