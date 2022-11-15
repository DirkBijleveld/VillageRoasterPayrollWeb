from pydantic import BaseModel


class LocationSchema(BaseModel):
    slug: str
    id: int = None

    class Config:
        orm_mode = True
