from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    primary_location_id = Column(Integer, ForeignKey("locations.id"))

    primary_location = relationship("Location", back_populates="employees")
