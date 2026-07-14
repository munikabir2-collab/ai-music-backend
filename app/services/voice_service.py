import os
import uuid
import pyttsx3

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def generate_voice(lyrics: str, voice: str = "female"):

    filename = f"voice_{uuid.uuid4().hex}.wav"

    filepath = os.path.join(
        UPLOAD_DIR,
        filename
    )


    try:

        engine = pyttsx3.init()


        voices = engine.getProperty("voices")


        if voice.lower() == "female":

            for v in voices:

                name = v.name.lower()

                if (
                    "female" in name
                    or "zira" in name
                    or "hazel" in name
                ):
                    engine.setProperty(
                        "voice",
                        v.id
                    )
                    break


        elif voice.lower() == "male":

            for v in voices:

                name = v.name.lower()

                if (
                    "male" in name
                    or "david" in name
                    or "mark" in name
                ):
                    engine.setProperty(
                        "voice",
                        v.id
                    )
                    break



        engine.setProperty(
            "rate",
            150
        )

        engine.setProperty(
            "volume",
            1.0
        )


        engine.save_to_file(
            lyrics,
            filepath
        )

        engine.runAndWait()



        return {
            "success": True,
            "file": filename,
            "voice": voice,
            "url": f"/uploads/{filename}"
        }



    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }