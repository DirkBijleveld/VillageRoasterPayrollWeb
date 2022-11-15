from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"))

    location = relationship("Location", back_populates="roles")
