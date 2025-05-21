from fastapi import FastAPI, UploadFile, File
from src.backend.whisper_utils import transcribe_audio
from src.backend.gpt_utils import summarize_text
import os

app = FastAPI()

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
