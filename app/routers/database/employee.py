from fastapi import APIRouter, Depends

from app.database import employees as db_emp

from app.dependencies import get_db
from app.schemas.employees import EmployeeSchema

router = APIRouter(prefix="/db/employees", tags=["employees"])


@router.get("/")
async def get_employees(session=Depends(get_db)):
    return db_emp.get_employees(session)


@router.get("/get/{employee_id}")
async def get_employee(employee_id: int, session=Depends(get_db)):
    return db_emp.get_employee(session, employee_id)


@router.post("/create")
async def create_employee(employee: EmployeeSchema, session=Depends(get_db)):
    return db_emp.make_employee(session, employee)


@router.post("/update")
async def update_employee(
    employee_id: int, employee: EmployeeSchema, session=Depends(get_db)
):
    return db_emp.update_employee(session, employee_id, employee)
