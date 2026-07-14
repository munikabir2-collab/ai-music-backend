from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import RegisterSchema, LoginSchema
from app.core.security import hash_password, verify_password
from app.core.jwt_handler import create_access_token


def register_user(db: Session, user: RegisterSchema):

    existing_email = db.query(User).filter(User.email == user.email).first()

    if existing_email:
        return {"success": False, "message": "Email already exists"}

    existing_username = db.query(User).filter(User.username == user.username).first()

    if existing_username:
        return {"success": False, "message": "Username already exists"}

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "success": True,
        "message": "Registration Successful"
    }


def login_user(db: Session, user: LoginSchema):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        return None

    if not verify_password(user.password, db_user.hashed_password):
        return None
   

    token = create_access_token(
        {
            "sub": str(db_user.id),
            "email": db_user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }