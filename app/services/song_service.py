import traceback

from app.services.lyrics_service import generate_lyrics
from app.services.musicgen_service import generate_music


def generate_complete_song(
    prompt: str,
    duration: int = 10,
    genre: str = "Pop"
):

    try:

        print("Generating lyrics...")

        lyrics = generate_lyrics(
            prompt=prompt,
            genre=genre
        )

        print("Lyrics generated successfully.")

        # Short prompt for MusicGen
        music_prompt = f"""
{genre} instrumental music.

Mood:
Inspirational, emotional, cinematic.

Theme:
{prompt}

High quality background music.
"""

        print("Generating instrumental music...")

        music_file = generate_music(
            prompt=music_prompt,
            duration=duration
        )

        print("Music generated successfully.")

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