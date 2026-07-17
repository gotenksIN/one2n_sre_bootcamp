import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SECRET_KEY = os.getenv("SECRET_KEY")
