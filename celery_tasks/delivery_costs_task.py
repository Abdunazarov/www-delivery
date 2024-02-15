# stdlib
import requests

# thirdparty
from sqlalchemy import select

from celery_worker import app
from db.db_setup import Session

# project
from db.models.parcel_model import Parcel
from settings import CURRENCY_API


@app.task
def update_delivery_costs():
    try:
        with Session.begin() as session:
            query = select(Parcel).filter(Parcel.delivery_cost.is_(None))
            parcels = session.execute(query).scalars().all()

            response = requests.get(CURRENCY_API)
            rates = response.json()
            usd_to_rub = rates["Valute"]["USD"]["Value"]

            for parcel in parcels:
                parcel.delivery_cost = (parcel.weight * 0.5 + parcel.content_value * 0.01) * usd_to_rub
                session.add(parcel)

            session.commit()

        return {"success": f"Number of calculated parcels: {len(parcels)}"}

    except Exception as e:
        print(e)
