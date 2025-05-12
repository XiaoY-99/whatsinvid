import whisper

model = whisper.load_model("base")  # or "small", "medium", "large"

def transcribe_audio(filepath: str) -> str:
    result = model.transcribe(filepath)
    return result["text"]
