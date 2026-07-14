import os
import uuid
import subprocess
import traceback

import torch
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

model = None


def get_model():
    global model

    if model is None:
        print("Loading MusicGen model...")

        model = MusicGen.get_pretrained("facebook/musicgen-small")

        # CPU only
        model.to("cpu")

        print("MusicGen Ready")

    return model


def generate_music(prompt: str, duration: int = 10):

    try:

        music_model = get_model()

        duration = max(5, min(duration, 30))

        music_model.set_generation_params(
            duration=duration,
            temperature=1.0,
            top_k=250,
            top_p=0.0,
            cfg_coef=3.0
        )

        print("=" * 50)
        print("Music Prompt:")
        print(prompt)
        print("=" * 50)

        with torch.no_grad():
            wav = music_model.generate([prompt])

        file_id = uuid.uuid4().hex

        wav_path = os.path.join(
            UPLOAD_DIR,
            f"music_{file_id}"
        )

        audio_write(
            wav_path,
            wav[0].cpu(),
            music_model.sample_rate,
            strategy="loudness"
        )

        wav_file = wav_path + ".wav"
        mp3_file = wav_path + ".mp3"

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                wav_file,
                "-codec:a",
                "libmp3lame",
                "-qscale:a",
                "2",
                mp3_file
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if os.path.exists(wav_file):
            os.remove(wav_file)

        print("Generated:", os.path.basename(mp3_file))

        return os.path.basename(mp3_file)

    except Exception:
        traceback.print_exc()
        raise