import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///meetings.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
    LLM_MODEL = os.environ.get('LLM_MODEL', 'openai/gpt-3.5-turbo')
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25MB file limit