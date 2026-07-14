import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_song_data(prompt: str):

    response = client.responses.create(
        model="gpt-5.5",
        input=f"""
Generate ONLY valid JSON.

Prompt:
{prompt}

Return this format:

{{
    "genre": "",
    "mood": "",
    "instruments": "",
    "lyrics": ""
}}
"""
    )

    return json.loads(
        response.output_text
    )