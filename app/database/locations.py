from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.locations import Location
from app.schemas.locations import LocationSchema


def get_location(db: Session, location_id: int) -> Location:
    """
    Retrieve a location by ID.
    """
    return db.execute(select(Location).where(Location.id == location_id)).scalar()


def get_locations(db: Session) -> list[Location]:
    """
    Retrieve all locations.
    """
    return db.execute(select(Location)).scalars().all()


def make_location(db: Session, location_schema: LocationSchema) -> Location:
    """
    Create a new location. Uses the pydantic LocationSchema.
    """
    location = Location(**location_schema.dict())
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def update_location(
    db: Session, location_id: int, location_schema: LocationSchema
) -> Location:
    """
    Updates all fields of a location. Uses the pydantic LocationSchema.
    """
    location = get_location(db, location_id)

    # For loop ensures all attributes in the location_schema are updated
    # in the Location as well. This is useful if the LocationSchema is
    # updated with new fields.
    for field in location_schema.dict():
        setattr(location, field, getattr(location_schema, field))

    # Commits changes to the database and refreshes the location object.
    db.commit()
    db.refresh(location)
    return location
