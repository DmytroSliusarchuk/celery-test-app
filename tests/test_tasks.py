import time

from app.tasks import fetch_users, fetch_address, fetch_credit_card
from app.models import User
from app.db import Session


def test_fetch_users():
    fetch_users()
    db = Session()
    users = db.query(User).all()
    assert len(users) == 10


def test_fetch_address(create_users):
    time.sleep(10)
    fetch_address()
    db = Session()
    users_without_address = (
        db.query(User).filter(User.address.is_(None)).count()
    )
    assert users_without_address == 0


def test_fetch_credit_card(create_users):
    time.sleep(10)
    fetch_credit_card()
    db = Session()
    users_without_credit_card = (
        db.query(User).filter(User.credit_card.is_(None)).count()
    )
    assert users_without_credit_card == 0
