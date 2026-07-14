import os
import uuid
import shutil
import subprocess

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def mix_song(
    instrumental_path: str,
    voice_path: str,
) -> str:

    if not os.path.exists(instrumental_path):
        raise FileNotFoundError(
            f"Music file not found: {instrumental_path}"
        )

    if not os.path.exists(voice_path):
        raise FileNotFoundError(
            f"Voice file not found: {voice_path}"
        )

    ffmpeg = shutil.which("ffmpeg")

    if ffmpeg is None:
        raise Exception(
            "FFmpeg is not installed or not added to PATH."
        )

    output_file = f"final_song_{uuid.uuid4().hex}.wav"

    output_path = os.path.join(
        UPLOAD_DIR,
        output_file
    )

    command = [
        ffmpeg,
        "-y",

        "-i", instrumental_path,
        "-i", voice_path,

        "-filter_complex",
        "[0:a]volume=0.45[music];"
        "[1:a]volume=1.8[voice];"
        "[music][voice]amix=inputs=2:duration=longest,"
        "loudnorm",

        "-ar", "44100",
        "-ac", "2",

        output_path,
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        print(result.stderr)
        raise Exception(result.stderr)

    print("Final song created:", output_file)

    return output_file