from fastapi import APIRouter
from app.services.voice_service import generate_voice


router = APIRouter(
    prefix="/voice",
    tags=["Voice"]
)


@router.post("/generate")
def create_voice(data: dict):

    lyrics = data.get("lyrics", "")
    voice = data.get("voice", "female")

    result = generate_voice(
        lyrics=lyrics,
        voice=voice
    )

    return result