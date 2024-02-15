# stdlib
from typing import Optional

# thirdparty
from pydantic import BaseModel, field_validator


class ParcelResponse(BaseModel):
    id: int
    delivery_cost: Optional[float] = str
    name: str
    weight: float
    type_id: int
    content_value: float

    @field_validator("delivery_cost")
    def validate_delivery_cost(cls, value):
        return "Not calculated" if value is None else value


class ParcelCreate(BaseModel):
    name: str
    weight: float
    type_id: int
    content_value: float


class ParcelTypeResponse(BaseModel):
    id: int
    name: str
