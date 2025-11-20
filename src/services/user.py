from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from dao import UserDao


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_dao = UserDao(session)
    
    async def get_user(self, tg_id: int) -> User | None:
        return await self.user_dao.find_by_tg_id(tg_id)
    
    async def create_user(
        self,
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
        return await self.user_dao.create(user_data)
    
    async def update_user(
        self,
        tg_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None
    ) -> User | None:
        update_data = {}
        if username is not None:
            update_data["username"] = username
        if first_name is not None:
            update_data["first_name"] = first_name
        if last_name is not None:
            update_data["last_name"] = last_name
        
        return await self.user_dao.update_by_tg_id(tg_id, update_data)
    
    async def upsert_user(
        self,
        tg_id: int,
        username: str | None,
        first_name: str,
        last_name: str | None = None
    ) -> User:
        user_data = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name
        }
        return await self.user_dao.upsert(tg_id, user_data)
