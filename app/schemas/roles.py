from pydantic import BaseModel


class RoleSchema(BaseModel):
    name: str
    location_id: int
    id: int = None

    class Config:
        orm_mode = True
