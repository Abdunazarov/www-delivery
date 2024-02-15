# stdlib
from typing import List

# thirdparty
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from celery_tasks.delivery_costs_task import update_delivery_costs

# project
from db.db_setup import get_session
from db.schemas.parcel_schemas import ParcelCreate, ParcelResponse, ParcelTypeResponse
from services.parcel_service import (
    create_parcel,
    get_parcel,
    get_parcel_types,
    get_parcels,
    get_type_by_id,
)

router = APIRouter(prefix="/parcels", tags=["PARCELS"])


@router.post("", response_model=ParcelResponse)
async def create_new_parcel(parcel: ParcelCreate, session: AsyncSession = Depends(get_session)):
    """
    Create a new parcel
    """
    parcel_type = await get_type_by_id(session=session, type_id=parcel.type_id)

    if not parcel_type:
        raise HTTPException(status_code=404, detail="Type not found")

    return await create_parcel(session=session, parcel=parcel)


@router.get("/types", response_model=List[ParcelTypeResponse])
async def get_all_parcel_types(session: AsyncSession = Depends(get_session)):
    """
    Get all parcel types
    """
    return await get_parcel_types(session=session)


@router.get("", response_model=List[ParcelResponse])
async def get_all_parcels(page: int = 1, limit: int = 10, session: AsyncSession = Depends(get_session)):
    """
    Get all parcels
    """
    parcels = await get_parcels(session, page=page, limit=limit)
    return parcels


@router.get("/{parcel_id}", response_model=ParcelResponse)
async def get_one_parcel(parcel_id: int, session: AsyncSession = Depends(get_session)):
    """
    Get one parcel by id
    """
    parcel = await get_parcel(session, parcel_id=parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")

    return parcel


@router.post("/calculate-delivery-cost", response_model=dict)
async def run_delivery_cost_calculation():
    """
    Run the task to calculate devlivery cost for parcels
    """
    update_delivery_costs.delay()
    return {"success": "Delivery cost calculated"}
