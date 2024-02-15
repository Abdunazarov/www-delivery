# thirdparty
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# project
from db.models.parcel_model import Parcel, ParcelType
from db.schemas.parcel_schemas import ParcelCreate


async def create_parcel(session: AsyncSession, parcel: ParcelCreate):
    query = insert(Parcel).values(**parcel.model_dump()).returning(Parcel)
    result = await session.execute(query)

    return result.scalar()


async def get_parcels(session: AsyncSession, page: int, limit: int):
    query = select(Parcel).offset((page - 1) * limit).limit(limit)
    result = await session.execute(query)

    return result.scalars().all()


async def get_parcel(session: AsyncSession, parcel_id: int):
    query = select(Parcel).filter(Parcel.id == parcel_id)
    result = await session.execute(query)

    return result.scalar()


async def get_type_by_id(session: AsyncSession, type_id: int):
    query = select(ParcelType).filter(ParcelType.id == type_id)

    result = await session.execute(query)
    return result.scalar()


async def get_parcel_types(session: AsyncSession):
    result = await session.execute(select(ParcelType))

    return result.scalars().all()
