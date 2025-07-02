import whisper
import os
from moviepy.video.io.VideoFileClip import VideoFileClip

model = whisper.load_model("base")  # or "small", "medium", etc.

def extract_audio_from_video(video_path: str) -> str:
    clip = VideoFileClip(video_path)
    audio_path = video_path.rsplit('.', 1)[0] + ".wav"
    clip.audio.write_audiofile(audio_path)
    return audio_path

def transcribe_audio(filepath: str) -> str:
    # If video, extract audio
    if filepath.lower().endswith((".mp4", ".mov", ".mkv", ".avi")):
        filepath = extract_audio_from_video(filepath)

    result = model.transcribe(filepath)
    return result["text"]
