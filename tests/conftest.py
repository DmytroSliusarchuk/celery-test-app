import pytest

from app import User
from app.db import Session
from app.tasks import fetch_users


@pytest.fixture(scope="function")
def db_session():
    session = Session()

    yield session

    session.close()


@pytest.fixture(scope="function")
def create_users(db_session):
    fetch_users()

    yield db_session.query(User).all()

    db_session.query(User).delete()
