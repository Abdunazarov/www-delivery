# thirdparty
from fastapi import FastAPI

# project
from routers import parcels

app = FastAPI(title="WWW Delivery")


# ADMIN ENDPOINTS
app.include_router(parcels.router)
