from fastapi import APIRouter, UploadFile, File, Depends,  HTTPException
from sqlalchemy.orm import Session
import shutil
import os

from fastapi.responses import FileResponse
from app.database.database import get_db
from app.models.song import Song

router = APIRouter(
    prefix="/songs",
    tags=["Songs"]
)

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


# Upload Song API
@router.post("/upload")
async def upload_song(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    song = Song(
        title=file.filename,
        filename=file.filename,
        filepath=file_path
    )

    db.add(song)
    db.commit()
    db.refresh(song)

    return {
        "message": "Song uploaded successfully",
        "id": song.id,
        "filename": song.filename
    }


# Song List API
@router.get("/")
def get_songs(db: Session = Depends(get_db)):
    songs = db.query(Song).all()

    return [
        {
            "id": song.id,
            "title": song.title,
            "filename": song.filename,
            "filepath": song.filepath
        }
        for song in songs
    ]


# Song Play API  👇 इसे यहीं add करें
@router.get("/{song_id}/play")
def stream_song(
    song_id: int,
    db: Session = Depends(get_db)
):
    song = db.query(Song).filter(Song.id == song_id).first()

    if not song:
        raise HTTPException(
            status_code=404,
            detail="Song not found"
        )

    if not os.path.exists(song.filepath):
        raise HTTPException(
            status_code=404,
            detail=f"File not found: {song.filepath}"
        )

    return FileResponse(
        path=song.filepath,
        media_type="audio/mpeg",
        filename=song.filename
    )



# Delete Song API
@router.delete("/{song_id}")
def delete_song(
    song_id: int,
    db: Session = Depends(get_db)
):
    # Database se song find karo
    song = db.query(Song).filter(Song.id == song_id).first()

    if not song:
        raise HTTPException(
            status_code=404,
            detail="Song not found"
        )

    # File delete karo
    if os.path.exists(song.filepath):
        os.remove(song.filepath)

    # Database record delete karo
    db.delete(song)
    db.commit()

    return {
        "message": "Song deleted successfully",
        "deleted_song_id": song_id
    }    