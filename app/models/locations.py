from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)
    roles = relationship("Role", back_populates="location")
    employees = relationship("Employee", back_populates="primary_location")
