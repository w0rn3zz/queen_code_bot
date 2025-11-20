from typing import Type, TypeVar, Generic

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseDao(Generic[ModelType]):
    model: Type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, obj: dict) -> ModelType:
        model_in = self.model(**obj)
        self.session.add(model_in)
        await self.session.flush()
        await self.session.refresh(model_in)
        return model_in

    async def find_by_id(self, model_id: int) -> ModelType | None:
        query = select(self.model).where(self.model.id == model_id)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def find_all_by_filters(self, filters: dict) -> list[ModelType]:
        query = select(self.model).filter_by(**filters)
        res = await self.session.execute(query)
        return list(res.scalars().all())

    async def find_one_by_filters(self, filters: dict) -> ModelType | None:
        query = select(self.model).filter_by(**filters)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def find_all(self) -> list[ModelType]:
        query = select(self.model)
        res = await self.session.execute(query)
        return list(res.scalars().all())

    async def update(self, filters: dict, values: dict) -> ModelType | None:
        query = (
            update(self.model).filter_by(**filters).values(**values).returning(self.model)
        )
        out_obj = await self.session.execute(query)
        return out_obj.scalar_one_or_none()

    async def update_by_id(self, model_id: int, values: dict) -> ModelType | None:
        query = (
            update(self.model)
            .where(self.model.id == model_id)
            .values(**values)
            .returning(self.model)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def count(self, filters: dict | None = None) -> int:
        query = select(func.count()).select_from(self.model)
        if filters:
            query = query.filter_by(**filters)
        result = await self.session.execute(query)
        return result.scalar()

    async def delete_by_id(self, model_id: int) -> None:
        query = delete(self.model).where(self.model.id == model_id)
        await self.session.execute(query)