import os
import uuid
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from whisper_utils import transcribe_audio
from gpt_utils import summarize_text
from translation_utils import translate_text
from slide_maker import generate_slides
from subtitle_utils import generate_srt_and_txt
from poster_gen import generate_poster

# Initialize FastAPI app
app = FastAPI()

# Allow frontend origin (adjust domain if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://whatsinvid.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if not exists
BASE_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Health check
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
    input_path = os.path.join(UPLOAD_DIR, f"{uid}_{filename_base}.mp3")

    with open(input_path, "wb") as f:
        f.write(await file.read())

    transcript = transcribe_audio(input_path)
    summary = summarize_text(transcript, language=language, tone=tone)

    summary_filename = f"{uid}_{filename_base}_summary.txt"
    summary_path = os.path.join(UPLOAD_DIR, summary_filename)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    return {
        "message": f"Summary generated in {language} with {tone} tone",
        "summary_path": f"uploads/{summary_filename}"
    }


@app.post("/subtitles/")
async def create_subtitles(
    file: UploadFile = File(...),
    language: str = Form("English")
):
    uid = str(uuid.uuid4())
    filename_base = os.path.splitext(file.filename)[0]
    input_path = os.path.join(UPLOAD_DIR, f"{uid}_{filename_base}.mp3")

    with open(input_path, "wb") as f:
        f.write(await file.read())

    transcript = transcribe_audio(input_path)
    if language.lower() != "english":
        transcript = translate_text(transcript, language)

    base_output = os.path.join(UPLOAD_DIR, f"{uid}_{filename_base}")
    paths = generate_srt_and_txt(transcript, base_output)

    return {
        "message": f"Subtitles generated in {language}",
        "srt_path": f"uploads/{os.path.basename(paths['srt'])}",
        "txt_path": f"uploads/{os.path.basename(paths['txt'])}"
    }


@app.post("/slides/")
async def create_slides(
    file: UploadFile = File(...),
    language: str = Form("English"),
    tone: str = Form("neutral")
):
    uid = str(uuid.uuid4())
    filename_base = os.path.splitext(file.filename)[0]
    input_path = os.path.join(UPLOAD_DIR, f"{uid}_{filename_base}.mp3")

    with open(input_path, "wb") as f:
        f.write(await file.read())

    transcript = transcribe_audio(input_path)
    summary = summarize_text(transcript, language=language, tone=tone)

    slide_filename = f"{uid}_{filename_base}_slides.pptx"
    slide_path = os.path.join(UPLOAD_DIR, slide_filename)
    generate_slides(summary, slide_path)

    return {
        "message": f"Slides generated in {language} with {tone} tone",
        "path": f"uploads/{slide_filename}"
    }


@app.post("/poster/")
async def create_poster(
    file: UploadFile = File(...),
    language: str = Form("English"),
    tone: str = Form("neutral")
):
    uid = str(uuid.uuid4())
    filename_base = os.path.splitext(file.filename)[0]
    input_path = os.path.join(UPLOAD_DIR, f"{uid}_{filename_base}.mp3")

    with open(input_path, "wb") as f:
        f.write(await file.read())

    transcript = transcribe_audio(input_path)
    summary = summarize_text(transcript, language=language, tone=tone)

    poster_filename = f"{uid}_{filename_base}_poster.png"
    poster_path = os.path.join(UPLOAD_DIR, poster_filename)
    generate_poster(summary, poster_path)

    return {
        "message": f"Poster generated in {language} with {tone} tone",
        "path": f"uploads/{poster_filename}"
    }


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    return FileResponse(
        file_path,
        filename=filename,
        media_type='application/octet-stream'
    )


# Make the uploads folder publicly accessible via /uploads/*
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
