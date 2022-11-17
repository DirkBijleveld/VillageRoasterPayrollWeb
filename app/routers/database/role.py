from fastapi import APIRouter, Depends

from app.database import roles as db_role

from app.dependencies import get_db
from app.schemas.roles import RoleSchema

router = APIRouter(prefix="/db/roles", tags=["roles"])


# GET Requests
@router.get("/")
async def get_roles(session=Depends(get_db)):
    return db_role.get_roles(session)


@router.get("/get/{role_id}")
async def get_role(role_id: int, session=Depends(get_db)):
    return db_role.get_role(session, role_id)


# POST Requests
@router.post("/create")
async def create_role(role: RoleSchema, session=Depends(get_db)):
    return db_role.make_role(session, role)


@router.post("/update")
async def update_role(role_id: int, role: RoleSchema, session=Depends(get_db)):
    return db_role.update_role(session, role_id, role)
