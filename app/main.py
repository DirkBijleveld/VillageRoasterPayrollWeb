from fastapi import FastAPI

from app.database.database import Base, engine
from app.routers.database import employee, location, role

app = FastAPI()

app.include_router(location.router)
app.include_router(employee.router)
app.include_router(role.router)


Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
