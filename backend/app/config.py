import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/hk_leaderboard')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET', 'super-secret-key')
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}
    JWT_ACCESS_TOKEN_EXPIRES = False