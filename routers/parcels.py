# stdlib
from typing import List

# thirdparty
from fastapi import APIRouter, Depends, HTTPException, Path, Query
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


@router.post("", response_model=ParcelResponse, summary="Create a new parcel")
async def create_new_parcel(parcel: ParcelCreate, session: AsyncSession = Depends(get_session)):
    """
    Creates a new parcel with the given parcel information.

    - **parcel**: _ParcelCreate_ - Parcel information to be created.
    """
    parcel_type = await get_type_by_id(session=session, type_id=parcel.type_id)

    if not parcel_type:
        raise HTTPException(status_code=404, detail="Parcel type not found")

    return await create_parcel(session=session, parcel=parcel)


@router.get("/types", response_model=List[ParcelTypeResponse], summary="List all parcel types")
async def get_all_parcel_types(session: AsyncSession = Depends(get_session)):
    """
    Retrieves a list of all available parcel types.
    """
    return await get_parcel_types(session=session)


@router.get("", response_model=List[ParcelResponse], summary="List parcels")
async def get_all_parcels(
    page: int = Query(1, description="Page number of the parcels list"),
    limit: int = Query(10, description="Number of parcels to return per page"),
    session: AsyncSession = Depends(get_session),
):
    """
    Retrieves a paginated list of parcels.

    - **page**: _int_ - Page number of the parcels list.
    - **limit**: _int_ - Number of parcels to return per page.
    """
    parcels = await get_parcels(session, page=page, limit=limit)
    return parcels


@router.get("/{parcel_id}", response_model=ParcelResponse, summary="Get a single parcel")
async def get_one_parcel(
    parcel_id: int = Path(..., description="The ID of the parcel to retrieve"),
    session: AsyncSession = Depends(get_session),
):
    """
    Retrieves a single parcel by its ID.

    - **parcel_id**: _int_ - The ID of the parcel to retrieve.
    """
    parcel = await get_parcel(session, parcel_id=parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")

    return parcel


@router.post("/calculate-delivery-cost", response_model=dict, summary="Calculate delivery costs")
async def run_delivery_cost_calculation():
    """
    Triggers a background task to calculate delivery costs for all parcels.
    """
    update_delivery_costs.delay()
    return {"success": "Delivery cost calculation task started"}
