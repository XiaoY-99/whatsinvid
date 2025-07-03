import os
import uuid
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from whisper_utils import transcribe_audio
from gpt_utils import summarize_text
from translation_utils import translate_text
from slide_maker import generate_slides
from subtitle_utils import generate_srt_and_txt
from poster_gen import generate_poster

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

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/summary/")
async def create_summary(
    file: UploadFile = File(...),
    language: str = Form("English"),
    tone: str = Form("neutral")
):
    uid = str(uuid.uuid4())
    filename_base = os.path.splitext(file.filename)[0]
    filepath = os.path.join(UPLOAD_DIR, f"{uid}_{filename_base}.mp3")

    with open(filepath, "wb") as f:
        f.write(await file.read())

    transcript = transcribe_audio(filepath)
    summary = summarize_text(transcript, language=language, tone=tone)

    summary_path = os.path.join(UPLOAD_DIR, f"{uid}_{filename_base}_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    return {
        "message": f"Summary generated in {language} with {tone} tone",
        "summary_path": summary_path
    }

@app.post("/subtitles/")
async def create_subtitles(
    file: UploadFile = File(...),
    language: str = Form("English")
):
    uid = str(uuid.uuid4())
    filename_base = os.path.splitext(file.filename)[0]
    filepath = os.path.join(UPLOAD_DIR, f"{uid}_{filename_base}.mp3")

    with open(filepath, "wb") as f:
        f.write(await file.read())

    transcript = transcribe_audio(filepath)
    if language.lower() != "english":
        transcript = translate_text(transcript, language)

    base_output_path = os.path.join(UPLOAD_DIR, f"{uid}_{filename_base}")
    paths = generate_srt_and_txt(transcript, base_output_path)

    return {
        "message": f"Subtitles generated in {language}",
        "srt_path": paths["srt"],
        "txt_path": paths["txt"]
    }

@app.post("/slides/")
async def create_slides(
    file: UploadFile = File(...),
    language: str = Form("English"),
    tone: str = Form("neutral")
):
    uid = str(uuid.uuid4())
    filename_base = os.path.splitext(file.filename)[0]
    filepath = os.path.join(UPLOAD_DIR, f"{uid}_{filename_base}.mp3")

    with open(filepath, "wb") as f:
        f.write(await file.read())

    transcript = transcribe_audio(filepath)
    summary = summarize_text(transcript, language=language, tone=tone)
    slide_path = os.path.join(UPLOAD_DIR, f"{uid}_slides.pptx")
    generate_slides(summary, slide_path)

    return {
        "message": f"Slides generated in {language} with {tone} tone",
        "path": slide_path
    }

@app.post("/poster/")
async def create_poster(
    file: UploadFile = File(...),
    language: str = Form("English"),
    tone: str = Form("neutral")
):
    uid = str(uuid.uuid4())
    filename_base = os.path.splitext(file.filename)[0]
    filepath = os.path.join(UPLOAD_DIR, f"{uid}_{filename_base}.mp3")

    with open(filepath, "wb") as f:
        f.write(await file.read())

    transcript = transcribe_audio(filepath)
    summary = summarize_text(transcript, language=language, tone=tone)
    poster_path = os.path.join(UPLOAD_DIR, f"{uid}_poster.png")
    generate_poster(summary, poster_path)

    return {
        "message": f"Poster generated in {language} with {tone} tone",
        "path": poster_path
    }
