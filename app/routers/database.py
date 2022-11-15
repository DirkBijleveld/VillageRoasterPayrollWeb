from fastapi import APIRouter, Depends

from app.schemas.locations import LocationSchema
from app.database import locations as db_loc
from app.database import employees as db_emp
from app.database import roles as db_role

from app.dependencies import get_db
from app.schemas.employees import EmployeeSchema
from app.schemas.roles import RoleSchema

router = APIRouter()


@router.post("/location/create")
async def create_location(location: LocationSchema, session=Depends(get_db)):
    return db_loc.make_location(session, location)


@router.get("/location/get/{location_id}")
async def get_location(location_id: int, session=Depends(get_db)):
    return db_loc.get_location(session, location_id)


@router.get("/locations")
async def get_locations(session=Depends(get_db)):
    return db_loc.get_locations(session)


@router.post("/location/update")
async def update_location(
    location_id: int, location: LocationSchema, session=Depends(get_db)
):
    return db_loc.update_location(session, location_id, location)


@router.post("/employee/create")
async def create_employee(employee: EmployeeSchema, session=Depends(get_db)):
    return db_emp.make_employee(session, employee)


@router.get("/employee/get/{employee_id}")
async def get_employee(employee_id: int, session=Depends(get_db)):
    return db_emp.get_employee(session, employee_id)


@router.get("/employees")
async def get_employees(session=Depends(get_db)):
    return db_emp.get_employees(session)


@router.post("/employee/update")
async def update_employee(
    employee_id: int, employee: EmployeeSchema, session=Depends(get_db)
):
    return db_emp.update_employee(session, employee_id, employee)


@router.post("/roles/create")
async def create_role(role: RoleSchema, session=Depends(get_db)):
    return db_role.make_role(session, role)


@router.get("/roles/get/{role_id}")
async def get_role(role_id: int, session=Depends(get_db)):
    return db_role.get_role(session, role_id)


@router.get("/roles")
async def get_roles(session=Depends(get_db)):
    return db_role.get_roles(session)


@router.post("/role/update")
async def update_role(role_id: int, role: RoleSchema, session=Depends(get_db)):
    return db_role.update_role(session, role_id, role)
