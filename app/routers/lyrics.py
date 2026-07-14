from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.lyrics_service import generate_lyrics

router = APIRouter(
    prefix="/lyrics",
    tags=["Lyrics"]
)


class LyricsRequest(BaseModel):
    prompt: str
    language: str = "Hindi"
    style: str = "Bollywood"


@router.post("/generate")
def create_lyrics(data: LyricsRequest):

    try:
        result = generate_lyrics(
            prompt=data.prompt,
            language=data.language,
            style=data.style
        )

        return {
            "lyrics": result
        }

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )