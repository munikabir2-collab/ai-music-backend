import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_lyrics(
    prompt: str,
    language: str = "Hindi",
    style: str = "Bollywood"
) -> str:

    response = client.responses.create(
        model="gpt-5.5",
        input=f"""
Write an ORIGINAL {style} song in {language}.

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
    )

    return response.output_text.strip()