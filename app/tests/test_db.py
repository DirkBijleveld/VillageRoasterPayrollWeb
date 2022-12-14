from fastapi.testclient import TestClient
from requests import Response

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from pytest import fixture

from app.database.database import Base
from app.dependencies import get_db
from app.main import app as main_app

from app.models.roles import Role
from app.models.locations import Location
from app.models.employees import Employee

# This is to remove import errors in PyCharm
# It performs no other purpose
if __name__ == "__main__":
    assert (Role, Location, Employee) is not None


# Testing uses in-memory SQLite database
SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

# Create a test database
engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# SessionLocal is instantiated to create a database session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """
    Overrides get_db() dependency to use the TestingSessionLocal
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app = main_app

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# The following fixtures relate to url pathing
@fixture
def db_url() -> str:
    return "/db"


@fixture
def loc_url(db_url) -> str:
    return f"{db_url}/locations"


@fixture
def emp_url(db_url) -> str:
    return f"{db_url}/employees"


@fixture
def role_url(db_url) -> str:
    return f"{db_url}/roles"


@fixture
def test_db():
    """
    Ensures that every test that uses the test_db fixture has a clean database.
    This + the in-memory SQLite database ensures that tests are independent of each other,
    and that they do not touch production.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@fixture
def fake_location_1(loc_url, test_db) -> Response:
    """
    Creates a Location in the database, and returns a TestClient response object.
    """
    yield client.post(f"{loc_url}/create", json={"slug": "test-slug-1"})


@fixture
def fake_location_2(loc_url, test_db) -> Response:
    """
    Creates a Location in the database, and returns a TestClient response object.
    """
    yield client.post(f"{loc_url}/create", json={"slug": "test-slug-2"})


@fixture
def fake_role(role_url, fake_location_1) -> Response:
    """
    Creates a Role in the database, and returns a TestClient response object.
    """
    yield client.post(
        f"{role_url}/create",
        json={"name": "test-role", "location_id": fake_location_1.json()["id"]},
    )


@fixture
def fake_employee_1(emp_url, fake_location_1) -> Response:
    """
    Creates an Employee in the database, and returns a TestClient response object.
    """
    yield client.post(
        f"{emp_url}/create",
        json={
            "name": "test-name-1",
            "primary_location_id": fake_location_1.json()["id"],
        },
    )


@fixture
def fake_employee_2(emp_url, fake_location_2) -> Response:
    """
    Creates a second Employee in the database, and returns a TestClient response object.
    """
    yield client.post(
        f"{emp_url}/create",
        json={
            "name": "test-name-2",
            "primary_location_id": fake_location_2.json()["id"],
        },
    )


def test_create_location(loc_url, test_db):
    """
    Tests Location creation. Does NOT use fake_location_1 fixture.
    """
    response = client.post(
        f"{loc_url}/create",
        json={"slug": "test-slug"},
    )
    assert response.status_code == 200
    assert response.json()["slug"] == "test-slug"


def test_get_location(loc_url, fake_location_1):
    """
    Tests Location retrieval. Uses fake_location_1 fixture.
    """
    location_id = fake_location_1.json()["id"]
    # GET request for Location json by location_id
    response = client.get(f"{loc_url}/get/{location_id}")
    assert response.status_code == 200
    assert response.json()["slug"] == fake_location_1.json()["slug"]


def test_get_locations(loc_url, fake_location_1, fake_location_2):
    """
    Tests multiple Location retrieval. Uses fake_location_1 and fake_location_2 fixtures.
    """
    response = client.get(f"{loc_url}")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["slug"] == fake_location_1.json()["slug"]
    assert response.json()[1]["slug"] == fake_location_2.json()["slug"]


def test_create_employee(emp_url, fake_location_1):
    """
    Tests Employee creation. Does NOT use fake_employee_1 fixture. Uses fake_location_1 fixture.
    """
    # Create an Employee
    response = client.post(
        f"{emp_url}/create",
        json={"name": "test-name", "primary_location_id": fake_location_1.json()["id"]},
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json()["name"] == "test-name"
    assert response.json()["primary_location_id"] == fake_location_1.json()["id"]


def test_get_employee(emp_url, fake_employee_1):
    """
    Tests Employee retrieval. Uses fake_employee_1 fixture.
    """
    employee_id = fake_employee_1.json()["id"]
    response = client.get(f"{emp_url}/get/{employee_id}")
    assert response.status_code == 200
    assert response.json()["name"] == fake_employee_1.json()["name"]
    assert (
        response.json()["primary_location_id"]
        == fake_employee_1.json()["primary_location_id"]
    )


def test_get_employees(emp_url, fake_employee_1, fake_employee_2):
    """
    Tests multiple Employee retrieval. Uses fake_employee_1 and fake_employee_2 fixtures.
    """
    response = client.get(f"{emp_url}")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == fake_employee_1.json()["name"]
    assert response.json()[1]["name"] == fake_employee_2.json()["name"]


def test_create_role(role_url, fake_location_1):
    """
    Tests Role creation. Does NOT use fake_role fixture. Uses fake_location_1 fixture.
    """
    # Create a Role
    response = client.post(
        f"{role_url}/create",
        json={"name": "test-role", "location_id": fake_location_1.json()["id"]},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "test-role"
    assert response.json()["location_id"] == fake_location_1.json()["id"]


def test_get_role(role_url, fake_role):
    """
    Tests Role retrieval. Uses fake_role fixture.
    """
    role_id = fake_role.json()["id"]
    response = client.get(f"{role_url}/get/{role_id}")
    assert response.status_code == 200
    assert response.json()["name"] == fake_role.json()["name"]
    assert response.json()["location_id"] == fake_role.json()["location_id"]


def test_get_roles(role_url, fake_role):
    """
    Tests multiple Role retrieval. Uses fake_role fixture.
    """
    response = client.get(f"{role_url}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == fake_role.json()["name"]
    assert response.json()[0]["location_id"] == fake_role.json()["location_id"]
