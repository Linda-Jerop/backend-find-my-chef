import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app import create_app, Base, get_db

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
# Using StaticPool so the in-memory SQLite database is shared across connections during tests
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    # Importing model modules to ensure they are registered with Base.metadata before creating tables.
    import app.models.user
    import app.models.chef
    import app.models.client
    import app.models.booking

    Base.metadata.create_all(bind=engine)  # Creating fresh tables for each test.
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)  # Clean up after test.


@pytest.fixture(scope="function")
def client(db_session):
    app = create_app()
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_user_data():
    return {
        "email": "testuser@example.com",
        "password": "SecurePass123!",
        "name": "Test User",
        "role": "client"
    }


@pytest.fixture
def sample_chef_data():
    return {
        "bio": "Experienced Italian chef",
        "cuisines": "Italian,French,Mediterranean",
        "hourly_rate": 50.0,
        "location": "Nairobi",
        "phone": "+254712345678",
        "years_of_experience": 10
    }


@pytest.fixture
def sample_booking_data():
    return {
        "booking_date": "2025-12-15",
        "booking_time": "18:00",
        "duration_hours": 3.0,
        "location": "123 Main St, Nairobi",
        "special_requests": "Please prepare vegetarian dishes"
    }
