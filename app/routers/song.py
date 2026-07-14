from fastapi import APIRouter
from pydantic import BaseModel

from app.services.song_service import generate_complete_song

router = APIRouter(
    prefix="/song",
    tags=["Song Generator"]
)


class SongRequest(BaseModel):
    prompt: str
    duration: int = 10
    genre: str = "Auto"


@router.post("/generate")
def generate_song(data: SongRequest):
    return generate_complete_song(
        prompt=data.prompt,
        duration=data.duration,
        genre=data.genre
    )