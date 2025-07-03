import os
import whisper
from moviepy.video.io.VideoFileClip import VideoFileClip
from typing import Optional

# Load Whisper model once at startup
model = whisper.load_model("base")  # Options: "tiny", "small", "medium", "large"

def extract_audio_from_video(video_path: str) -> str:
    """
    Extracts audio from a video file and saves it as a .wav file.
    Returns the path to the extracted audio.
    """
    try:
        clip = VideoFileClip(video_path)
        audio_path = video_path.rsplit('.', 1)[0] + ".wav"
        clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
        clip.close()
        return audio_path
    except Exception as e:
        raise RuntimeError(f"[Audio Extraction Error] Failed to extract audio: {e}")

def transcribe_audio(filepath: str, language: Optional[str] = None) -> str:
    """
    Transcribes a given audio or video file using Whisper.
    Converts video to audio automatically.
    
    Args:
        filepath (str): Path to the uploaded file
        language (Optional[str]): Language to guide Whisper (e.g., "en", "zh", "fr")
    
    Returns:
        str: Transcribed text
    """
    is_temp_audio = False
    original_path = filepath

    try:
        # Convert video formats to audio
        if filepath.lower().endswith((".mp4", ".mov", ".mkv", ".avi", ".webm", ".flv")):
            filepath = extract_audio_from_video(filepath)
            is_temp_audio = True

        # Whisper transcription
        result = model.transcribe(filepath, language=language if language else None)
        return result["text"]

    except Exception as e:
        raise RuntimeError(f"[Transcription Error] {e}")

    finally:
        # Cleanup temp audio file if created
        if is_temp_audio and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as cleanup_err:
                print(f"[WARN] Failed to remove temp audio file: {cleanup_err}")

        # Optional: cleanup original uploaded file
        if os.path.exists(original_path):
            try:
                os.remove(original_path)
            except Exception as original_cleanup_err:
                print(f"[WARN] Failed to remove uploaded file: {original_cleanup_err}")
