import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "default.env"))

class Settings:
    def __init__(self):
        self.APP_ENV = os.getenv("APP_ENV", "development")
        self.APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
        self.APP_PORT = int(os.getenv("APP_PORT", 8000))
        
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        self.EMAIL_USER = os.getenv("EMAIL_USER")
        self.EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
        self.EMAIL_SMTP = os.getenv("EMAIL_SMTP", "smtp.gmail.com")
        self.EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))

        self.WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

settings = Settings()

