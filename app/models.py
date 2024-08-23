from sqlalchemy import Column, Integer, String

from app.db import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    address = Column(String, nullable=True)
    credit_card = Column(String, nullable=True)
