## whatsinvid
App development for generating summaries/slides/poster/... of a video automatically. ;

## Set up
pip install -r requirements.txt

## Add a .env file --> config/default.env for example:
# FastAPI settings
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000

# OpenAI API
OPENAI_API_KEY=your-openai-key-here

# Email settings
EMAIL_USER=you@example.com
EMAIL_PASSWORD=your-email-password
EMAIL_SMTP=smtp.gmail.com
EMAIL_PORT=587

# Whisper settings
WHISPER_MODEL=base

## Run this command in the terminal to test OpenAI API:
PYTHONPATH=. pytest src/tests/test_openai.py -s
