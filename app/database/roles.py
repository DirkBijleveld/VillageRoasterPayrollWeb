from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.roles import Role
from app.schemas.roles import RoleSchema


def get_role(db: Session, role_id: int):
    stmt = select(Role).where(Role.id == role_id)
    return db.execute(stmt).scalar()


def get_roles(db: Session):
    stmt = select(Role)
    return db.execute(stmt).scalars().all()


def make_role(db: Session, role_schema: RoleSchema):
    role = Role(**role_schema.dict())
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def update_role(db: Session, role_id: int, role_schema: RoleSchema):
    role = get_role(db, role_id)
    role.name = role_schema.name
    role.location_id = role_schema.location_id
    db.commit()
    db.refresh(role)
    return role
