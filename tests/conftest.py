from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
import pytest
import os 

from app.core.config import ENV
from app.database.models import Base
from app.core.dependecies import get_session
from app.main import app

os.environ["TESTING"] = "1"

TEST_DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/tests_db"
test_engine = create_engine(TEST_DATABASE_URL)
test_session = sessionmaker(autoflush=False,bind=test_engine)

def get_test_db_session() :
    session = test_session()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="session",autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="module")
def client():

    app.dependency_overrides[get_session] = get_test_db_session

    with TestClient(app,raise_server_exceptions=True) as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture(scope="module")
def auth_headers(client):
    response = client.post("api/v1/login",params = {"username":"james007","password":"james007"})

    token = response.json()["access_token"]
    return {"Authorization":f"Bearer {token}"}