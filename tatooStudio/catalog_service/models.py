from sqlalchemy import Column, Integer, String, Numeric
from shared.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)  # Например, 99.99
    category = Column(String(100), nullable=False)