from fastapi import FastAPI

from app.database.database import Base, engine
from app.routers import database

app = FastAPI()
app.include_router(database.router, prefix="/database", tags=["database"])

Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
