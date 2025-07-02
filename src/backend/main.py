import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from src.backend.whisper_utils import transcribe_audio
from src.backend.gpt_utils import summarize_text
from src.backend.slide_maker import generate_slides
from src.backend.subtitle_utils import generate_srt
from src.backend.poster_gen import generate_poster

# Initialize FastAPI app
app = FastAPI()

# Allow frontend origin (update if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://whatsinvid.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    transcript = transcribe_audio(filepath)
    summary = summarize_text(transcript)

    return {"transcript": transcript, "summary": summary}

@app.post("/slides/")
async def create_slides(file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    transcript = transcribe_audio(filepath)
    summary = summarize_text(transcript)
    slide_path = os.path.join(UPLOAD_DIR, "slides.pptx")
    generate_slides(summary, slide_path)

    return {"message": "Slides generated", "path": slide_path}

@app.post("/subtitles/")
async def create_subtitles(file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    transcript = transcribe_audio(filepath)
    srt_path = os.path.join(UPLOAD_DIR, "subtitles.srt")
    generate_srt(transcript, srt_path)

    return {"message": "Subtitles generated", "path": srt_path}

@app.post("/poster/")
async def create_poster(file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    transcript = transcribe_audio(filepath)
    summary = summarize_text(transcript)
    poster_path = os.path.join(UPLOAD_DIR, "poster.png")
    generate_poster(summary, poster_path)

    return {"message": "Poster generated", "path": poster_path}
