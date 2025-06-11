from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from shared.models import BookingCreate, BookingOut
from shared.auth import get_current_user
from shared.database import get_db
import models

app = FastAPI()

models.Base.metadata.create_all(bind=models.engine)


@app.post("/bookings", response_model=BookingOut)
def create_booking(booking: BookingCreate,
                   current_user: dict = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    # Добавляем ID пользователя из токена
    new_booking = models.Booking(**booking.dict(), user_id=current_user["user_id"])
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


@app.get("/bookings", response_model=list[BookingOut])
def get_bookings(current_user: dict = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    return db.query(models.Booking).filter(models.Booking.user_id == current_user["user_id"]).all()


@app.delete("/bookings/{booking_id}")
def cancel_booking(booking_id: int,
                   current_user: dict = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    booking = db.query(models.Booking).get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not allowed to delete this booking")
    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted"}