# thirdparty
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# project
from db.db_setup import Base


class Parcel(Base):
    __tablename__ = "parcels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    weight = Column(Float, nullable=False)
    type_id = Column(Integer, ForeignKey("parcel_types.id"), nullable=False)
    content_value = Column(Float, nullable=False)
    delivery_cost = Column(Float)


class ParcelType(Base):
    __tablename__ = "parcel_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    parcels = relationship("Parcel", backref="type")
