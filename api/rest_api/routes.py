"""
This file is responsible to define user routes
"""

from datetime import timedelta
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from api.rest_api.models import User, CreateUserRequest, AuthRequest
from api.config.auth import get_password_hash, verify_password, create_access_token
from api.config.db import SessionLocal, UserDB

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/health/",
    status_code=status.HTTP_200_OK,
)
def health_check(db: Session = Depends(get_db)):
    try:
        is_active_db = db.is_active
        if is_active_db:
            return {"message": "ok", "status_code": status.HTTP_200_OK}
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Health check failed")
        
    

@router.post(
    "/users/",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
def create_user(user: CreateUserRequest, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    existig_user = db.query(UserDB).filter(UserDB.email == user.email).all()
    if len(existig_user):
        return existig_user[0]
    db_user = UserDB(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User(id=db_user.id, name=db_user.name, email=db_user.email, hashed_password=db_user.hashed_password)


@router.post("/auth/token/")
def login(user: AuthRequest, db: Session = Depends(get_db)):
    try:
        db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(data={"sub": db_user.email}, expires_delta=timedelta(minutes=30))
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
