import os
from os import environ


class Config:
    SESSION_COOKIE_NAME = environ.get("SESSION_COOKIE_NAME")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MEDIA_FOLDER = os.environ["MEDIA_FOLDER"]  # We want the program to crash if the variable doesn't exist
    TRACK_METADATA = os.environ["TRACK_METADATA"]  # We want the program to crash if the variable doesn't exist


class ProductionConfig(Config):
    FLASK_ENV = "production"
    SECRET_KEY = environ.get("SECRET_KEY")
    DEBUG = False
    TESTING = False

    # TODO create this in the install directory of the app
    # SQLALCHEMY_DATABASE_URI = ""


class DevelopmentConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"


class TestingConfig(Config):
    FLASK_ENV = "testing"
    DEBUG = False
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
