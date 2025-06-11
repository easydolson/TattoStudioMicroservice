from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from shared.models import ServiceCreate, ServiceOut
from shared.auth import get_current_user
from shared.database import get_db
import models

app = FastAPI()

models.Base.metadata.create_all(bind=models.engine)


@app.post("/services", response_model=ServiceOut)
def create_service(service: ServiceCreate,
                   current_user: dict = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    new_service = models.Service(**service.dict())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service


@app.get("/services", response_model=list[ServiceOut])
def get_services(db: Session = Depends(get_db)):
    return db.query(models.Service).all()


@app.get("/services/{service_id}", response_model=ServiceOut)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(models.Service).get(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service