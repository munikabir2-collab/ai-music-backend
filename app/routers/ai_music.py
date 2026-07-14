from fastapi import APIRouter

from app.schemas.ai import MusicPrompt
from app.services.lyrics_service import generate_lyrics
from app.services.musicgen_service import generate_music

router = APIRouter()

@router.get("/")
def home():
    return {
        "message": "AI Music API"
    }

@router.post("/generate")
def generate(data: MusicPrompt):

    lyrics = generate_lyrics(
        prompt=data.prompt
    )

    music = generate_music(
        prompt=data.prompt,
        duration=data.duration
    )

    return {
        "success": True,
        "lyrics": lyrics,
        "music": music,
        "url": f"/uploads/{music}"
    }