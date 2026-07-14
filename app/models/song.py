from fastapi import APIRouter
from sqlalchemy import Column, Integer, String
from app.database.database import Base
router = APIRouter(
    prefix="/songs",
    tags=["Songs"]
)

@router.get("/")
def songs_home():
    return {"message": "Songs Router Working"}


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    filename = Column(String)
    filepath = Column(String)    