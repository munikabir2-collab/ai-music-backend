from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import os

from app.database.database import Base, engine
from app.routers import auth, users, songs, ai_music, voice
from app.routers import lyrics, song
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

Base.metadata.create_all(bind=engine)

# पहले app बनाइए
app = FastAPI(
    title="AI Music API",
    version="1.0.0",
    description="AI Music Backend with Auth, Users, Songs and AI Music Generation"
)

# उसके बाद CORS जोड़िए
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(songs.router)
app.include_router(ai_music.router)
app.include_router(lyrics.router)
app.include_router(voice.router)
app.include_router(song.router)





app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
    name="uploads"
)

@app.get("/")
def home():
    return {
        "message": "AI Music Backend Running Successfully 🚀"
    }

@app.get("/health")
def health():
    return {"status": "ok"}