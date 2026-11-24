from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from piazza_app.database import get_db
from piazza_app.schemas import (
    UserCreate,
    UserResponse,
    UserLogin,
    TokenResponse,
)
from piazza_app.security import hash_password, verify_password
from piazza_app.tokens import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    email = user_data.email.lower()

    existing_user = (
        db.query(User)
        .filter(or_(User.username == user_data.username, User.email == email))
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username or email is already registered",
        )

    user = User(
        username=user_data.username,
        email=email,
        hashed_password=hash_password(user_data.password),
    )

    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Username or email is already registered",
        )

    db.refresh(user)
    return user

@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    email = user_data.email.lower()

    user = db.query(User).filter(User.email == email).first()

    if user is None or not verify_password(
        user_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenResponse(
        access_token=create_access_token(user.id),
        token_type="bearer",
    )