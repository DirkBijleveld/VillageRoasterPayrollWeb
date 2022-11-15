from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.employees import Employee
from app.schemas.employees import EmployeeSchema


def get_employee(db: Session, employee_id: int):
    return db.execute(select(Employee).where(Employee.id == employee_id)).scalar_one()


def get_employees(db: Session):
    return db.execute(select(Employee)).scalars().all()


def make_employee(db: Session, employee_schema: EmployeeSchema):
    employee = Employee(**employee_schema.dict())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee(db: Session, employee_id: int, employee_schema: EmployeeSchema):
    employee = get_employee(db, employee_id)

    employee.name = employee_schema.name
    employee.primary_location_id = employee_schema.primary_location_id

    db.commit()
    db.refresh(employee)
    return employee
