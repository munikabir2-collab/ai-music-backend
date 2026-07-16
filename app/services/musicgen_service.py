import os
import time
import uuid
import shutil
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
        print("=" * 60)
        print("Loading MusicGen model...")
        print("=" * 60)

        model = MusicGen.get_pretrained("facebook/musicgen-small")

        # inference mode
        model.lm.eval()

        print("MusicGen Ready")
        print("=" * 60)

    return model


def generate_music(prompt: str, duration: int = 5):

    try:

        music_model = get_model()

        duration = max(3, min(duration, 8))

        music_model.set_generation_params(
            duration=duration,
            temperature=1.0,
            top_k=250,
            top_p=0.0,
            cfg_coef=3.0,
        )

        print("=" * 60)
        print("Music Prompt")
        print("=" * 60)
        print(prompt)

        print("=" * 60)
        print("Generating music...")
        print("=" * 60)

        start = time.time()

        with torch.inference_mode():
            wav = music_model.generate([prompt])

        print(f"Generation Finished in {time.time()-start:.2f} sec")

        file_id = uuid.uuid4().hex

        wav_path = os.path.join(
            UPLOAD_DIR,
            f"music_{file_id}"
        )

        print("Saving WAV...")

        audio_write(
            wav_path,
            wav[0].cpu(),
            music_model.sample_rate,
            strategy="loudness"
        )

        wav_file = wav_path + ".wav"
        mp3_file = wav_path + ".mp3"

        if not os.path.exists(wav_file):
            raise Exception("WAV file was not created.")

        print("Converting MP3...")

        ffmpeg = shutil.which("ffmpeg")

        if ffmpeg is None:
            raise Exception("FFmpeg not found in PATH")

        result = subprocess.run(
            [
                ffmpeg,
                "-y",
                "-i",
                wav_file,
                "-codec:a",
                "libmp3lame",
                "-qscale:a",
                "2",
                mp3_file,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(result.stderr)
            raise Exception("FFmpeg conversion failed")

        if os.path.exists(wav_file):
            os.remove(wav_file)

        if not os.path.exists(mp3_file):
            raise Exception("MP3 file not created")

        print("=" * 60)
        print("SUCCESS")
        print(mp3_file)
        print("=" * 60)

        return os.path.basename(mp3_file)

    except Exception as e:

        print("=" * 60)
        print("MUSIC GENERATION ERROR")
        print("=" * 60)
        traceback.print_exc()

        raise e