from pydantic import BaseModel


class EmployeeSchema(BaseModel):
    name: str
    primary_location_id: int
    id: int = None

    class Config:
        orm_mode = True
