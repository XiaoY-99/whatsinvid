from fastapi import FastAPI, UploadFile, File
from whisper_utils import transcribe_audio
from gpt_utils import summarize_text

app = FastAPI()

@app.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    filepath = f"uploads/{file.filename}"
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    transcript = transcribe_audio(filepath)
    summary = summarize_text(transcript)
    return {"transcript": transcript, "summary": summary}
