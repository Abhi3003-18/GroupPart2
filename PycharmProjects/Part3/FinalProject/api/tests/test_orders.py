from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..controllers import orders as controller
from ..dependencies.database import get_db, Base
from ..main import app
import pytest
from ..models import orders as model

TEST_DATABASE_URL = "sqlite:///./test.db"

# Set up the test database
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# TestClient for FastAPI app
client = TestClient(app)

# Set up the database before tests
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Test creating an order via the API
def test_create_order():
    order_data = {
        "customer_name": "John Doe",
        "description": "Test order"
    }

    response = client.post("/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert data["description"] == "Test order"

# Test fetching all orders via the API
def test_get_orders():
    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Ensure at least one order exists