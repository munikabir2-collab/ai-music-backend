import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_lyrics(
    prompt: str,
    language: str = "Hindi",
    genre: str = "Bollywood"
) -> str:

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a professional songwriter. Write only original song lyrics."
            },
            {
                "role": "user",
                "content": f"""
Write an ORIGINAL {genre} song in {language}.

Topic:
{prompt}

Format:

Title

Verse 1

Chorus

Verse 2

Bridge

Outro

Return ONLY the lyrics.
"""
            }
        ],
        temperature=0.9,
        max_tokens=1024,
    )

    return completion.choices[0].message.content.strip()