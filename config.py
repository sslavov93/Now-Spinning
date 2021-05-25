from os import environ


class Config:
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    FLASK_ENV = 'production'
    SECRET_KEY = environ.get('SECRET_KEY')
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = "sqlite:////Users/svet/Desktop/prod.db"


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////Users/svet/Desktop/persist.db"


class TestConfig(Config):
    FLASK_ENV = 'testing'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////Users/svet/Desktop/test.db"
