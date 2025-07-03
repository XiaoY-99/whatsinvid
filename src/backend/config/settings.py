import os
from dotenv import load_dotenv

# Load environment variables from default.env if available
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "default.env"))

class Settings:
    def __init__(self):
        # App environment
        self.APP_ENV = os.getenv("APP_ENV", "development")
        self.APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
        self.APP_PORT = int(os.getenv("APP_PORT", 8000))

        # API Keys and Services
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        # Email Settings
        self.EMAIL_USER = os.getenv("EMAIL_USER")
        self.EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
        self.EMAIL_SMTP = os.getenv("EMAIL_SMTP", "smtp.gmail.com")
        self.EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))

        # Whisper Model
        self.WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

        # URLs (Set these in Render/Vercel environment)
        self.FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
        self.BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

        # CORS
        self.ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", self.FRONTEND_URL).split(",")

settings = Settings()
