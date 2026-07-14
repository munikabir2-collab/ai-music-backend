from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import os


model = None


def get_model():

    global model

    if model is None:
        model = MusicGen.get_pretrained(
            "facebook/musicgen-small"
        )

        model.set_generation_params(
            duration=10
        )

    return model



def generate_ai_music(prompt: str):

    ai_model = get_model()


    wav = ai_model.generate(
        [prompt]
    )


    folder = "uploads/generated"

    os.makedirs(
        folder,
        exist_ok=True
    )


    file_name = "music.wav"

    path = f"{folder}/{file_name}"


    audio_write(
        f"{folder}/music",
        wav[0].cpu(),
        ai_model.sample_rate,
        strategy="loudness"
    )


    return path