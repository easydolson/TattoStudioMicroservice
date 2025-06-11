from sqlalchemy import Column, Integer, String
from shared.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    role = Column(String(50), default="client")