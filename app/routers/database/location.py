from fastapi import APIRouter, Depends

from app.schemas.locations import LocationSchema
from app.database import locations as db_loc

from app.dependencies import get_db

router = APIRouter(prefix="/db/locations", tags=["locations"])


@router.get("/")
async def get_locations(session=Depends(get_db)):
    return db_loc.get_locations(session)


@router.post("/create")
async def create_location(location: LocationSchema, session=Depends(get_db)):
    return db_loc.make_location(session, location)


@router.get("/get/{location_id}")
async def get_location(location_id: int, session=Depends(get_db)):
    return db_loc.get_location(session, location_id)


@router.post("/update")
async def update_location(
    location_id: int, location: LocationSchema, session=Depends(get_db)
):
    return db_loc.update_location(session, location_id, location)
