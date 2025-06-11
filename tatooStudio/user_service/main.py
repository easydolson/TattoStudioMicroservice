from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from shared.database import get_db
from shared.models import UserLogin, UserOut, Token
from shared.auth import create_access_token, get_current_user, get_password_hash, verify_password
import models

app = FastAPI()

# Создание таблиц при запуске
models.Base.metadata.create_all(bind=models.engine)


@app.post("/register", response_model=UserOut)
def register(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = models.User(username=user.username, password=hashed_password, role="client")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": str(db_user.id), "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile", response_model=UserOut)
def profile(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.User).get(current_user["user_id"])