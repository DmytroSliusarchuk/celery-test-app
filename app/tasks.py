import requests
import os

from dotenv import load_dotenv
from celery import Celery

from app.db import Session
from app.models import User

load_dotenv()

app = Celery("tasks", broker=os.getenv("CELERY_BROKER_URL"))


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(100, fetch_users.s(), name="fetch users")
    sender.add_periodic_task(130, fetch_address.s(), name="fetch address")
    sender.add_periodic_task(
        160, fetch_credit_card.s(), name="fetch credit card"
    )


@app.task
def fetch_users():
    with Session() as db:
        try:
            response = requests.get(
                "https://random-data-api.com/api/v2/users",
                params={"size": os.getenv("USERS_FETCH_SIZE")},
            )
            if response.status_code != 200:
                raise Exception(f"Failed to fetch users: {response.text}")

            users_data = response.json()

            for user_data in users_data:
                user_id = user_data["id"]
                if not db.query(User).filter(User.id == user_id).first():
                    new_user = User(
                        id=user_id,
                        name=user_data["first_name"]
                        + " "
                        + user_data["last_name"],
                        email=user_data["email"],
                    )
                    db.add(new_user)
            db.commit()
        except Exception as e:
            print(f"Error fetching users: {str(e)}")


@app.task
def fetch_address():
    with Session() as db:
        try:
            users_without_address = (
                db.query(User).filter(User.address.is_(None)).all()
            )

            response = requests.get(
                "https://random-data-api.com/api/v2/addresses",
                params={"size": len(users_without_address)},
            )
            if response.status_code != 200:
                raise Exception(f"Failed to fetch address: {response.text}")

            addresses_data = response.json()

            for user in users_without_address:
                address_data = addresses_data.pop()
                user.address = (
                    address_data["full_address"]
                    + ", "
                    + address_data["city"]
                    + ", "
                    + address_data["state"]
                    + ", "
                    + address_data["country"]
                )
            db.commit()
        except Exception as e:
            print(f"Error fetching address: {str(e)}")


@app.task
def fetch_credit_card():
    with Session() as db:
        try:
            users_without_credit_card = (
                db.query(User).filter(User.credit_card.is_(None)).all()
            )

            response = requests.get(
                "https://random-data-api.com/api/v2/credit_cards",
                params={"size": len(users_without_credit_card)},
            )
            if response.status_code != 200:
                raise Exception(
                    f"Failed to fetch credit card: {response.text}"
                )

            credit_cards_data = response.json()

            for user in users_without_credit_card:
                user.credit_card = credit_cards_data.pop()[
                    "credit_card_number"
                ]
            db.commit()
        except Exception as e:
            print(f"Error fetching credit card: {str(e)}")
