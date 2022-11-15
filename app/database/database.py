# Default FastAPI SQLAlchemy database setup
# From: https://fastapi.tiangolo.com/tutorial/sql-databases/
# Retrieved on 13/11/2022 for version 0.86.0

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
