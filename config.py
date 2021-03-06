import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    DEBUG = os.getenv("DEBUG")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Dropbox
    DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")
    DROPBOX_PATH = os.getenv("DROPBOX_PATH")

    # Paginate
    USER_PER_PAGE = 5

    # Flask-Login
    USE_SESSION_FOR_NEXT = False
