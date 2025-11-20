from typing import Type, TypeVar, Generic

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseDao(Generic[ModelType]):
    model: Type[ModelType]

    @classmethod
    async def create(cls, session: AsyncSession, obj: dict) -> Type[ModelType]:
        model_in = cls.model(**obj)
        session.add(model_in)
        await session.commit()
        await session.refresh(model_in)
        return model_in

    @classmethod
    async def find_by_id(cls, session: AsyncSession, model_id: int) -> Type[ModelType]:
        query = select(cls.model).where(cls.model.id == model_id)
        res = await session.execute(query)

        return res.scalar()

    @classmethod
    async def find_all_by_filters(
        cls, session: AsyncSession, filters: dict
    ) -> list[Type[ModelType]]:
        query = select(cls.model).filter_by(**filters)
        res = await session.execute(query)

        return list(res.scalars().all())

    @classmethod
    async def find_one_by_filters(
        cls, session: AsyncSession, filters: dict
    ) -> Type[ModelType]:
        query = select(cls.model).filter_by(**filters)
        res = await session.execute(query)

        return res.scalar()

    @classmethod
    async def find_all(cls, session: AsyncSession) -> list[Type[ModelType]]:
        query = select(cls.model)
        res = await session.execute(query)

        return list(res.scalars().all())

    @classmethod
    async def update(
        cls, session: AsyncSession, filters: dict, values: dict
    ) -> Type[ModelType]:
        query = (
            update(cls.model).filter_by(**filters).values(**values).returning(cls.model)
        )
        out_obj = await session.execute(query)
        await session.commit()
        return out_obj.scalar()

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, model_id: int) -> None:
        query = delete(cls.model).where(cls.model.id == model_id)
        await session.execute(query)
        await session.commit()