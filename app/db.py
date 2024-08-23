import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    try:
        inspector = inspect(engine)
        if not inspector.get_table_names():
            Base.metadata.create_all(bind=engine)
            print("Database initialized.")
        else:
            print("Database already initialized.")
    except Exception as e:
        print(
            "Error: Unable to connect to the database. Please check your connection settings."
        )
