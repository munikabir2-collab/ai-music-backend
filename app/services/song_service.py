import traceback

from app.services.lyrics_service import generate_lyrics
from app.services.musicgen_service import generate_music


def generate_complete_song(
    prompt: str,
    duration: int = 10,
    genre: str = "Auto"
):

    try:

        # 1. Generate lyrics using OpenAI
        lyrics = generate_lyrics(
            prompt=prompt,
            genre=genre
        )

        # 2. Better prompt for MusicGen
        music_prompt = f"""
Genre: {genre}

Song Theme:
{prompt}

Lyrics:
{lyrics}

Create an instrumental background music matching the lyrics.
"""

        # 3. Generate Instrumental
        music_file = generate_music(
            music_prompt,
            duration
        )

        return {
            "success": True,
            "prompt": prompt,
            "genre": genre,
            "lyrics": lyrics,
            "music": music_file,
            "url": f"/uploads/{music_file}"
        }

    except Exception as e:

        traceback.print_exc()

        return {
            "success": False,
            "error": str(e),
            "type": type(e).__name__
        }