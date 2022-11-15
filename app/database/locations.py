from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.locations import Location
from app.schemas.locations import LocationSchema

from app.models.roles import Role
from app.models.employees import Employee


def get_location(db: Session, location_id: int):
    stmt = select(Location).where(Location.id == location_id)
    return db.execute(stmt).scalar()


def get_locations(db: Session):
    stmt = select(Location)
    return db.execute(stmt).scalars().all()


def make_location(db: Session, location_schema: LocationSchema):
    location = Location(**location_schema.dict())
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def update_location(db: Session, location_id: int, location_schema: LocationSchema):
    location = get_location(db, location_id)
    location.slug = location_schema.slug
    db.commit()
    db.refresh(location)
    return location
