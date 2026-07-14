from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.schemas.auth import RegisterSchema, LoginSchema
from app.services.auth_service import register_user, login_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: RegisterSchema, db: Session = Depends(get_db)):
    result = register_user(db, user)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return result


@router.post("/login")
def login(user: LoginSchema, db: Session = Depends(get_db)):
    token = login_user(db, user)

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    return token


@router.get("/")
def home():
    return {
        "message": "Authentication API Running"
    }