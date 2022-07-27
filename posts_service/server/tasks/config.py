from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, "../.dockerenv"))


class Config:
    """Set Flask config variables."""

    FLASK_ENV = "development"
    TESTING = True
    ML_API = environ.get("ML_API")
    BROKER_URL = environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = environ.get("CELERY_RESULT_BACKEND")
