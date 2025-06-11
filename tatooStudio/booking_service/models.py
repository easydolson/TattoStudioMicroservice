from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from shared.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    date = Column(Date, nullable=False)

    # Опционально: связи для удобства работы с ORM
    user = relationship("User", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")


User.bookings = relationship("Booking", back_populates="user")
Service.bookings = relationship("Booking", back_populates="service")