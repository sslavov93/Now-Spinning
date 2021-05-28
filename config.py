from os import environ


class Config:
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    SECRET_KEY = environ.get('SECRET_KEY')
    DEBUG = False
    TESTING = False

    # TODO create this in the install directory of the app
    # SQLALCHEMY_DATABASE_URI = "sqlite:////Users/svet/Desktop/prod.db"


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"


class TestingConfig(Config):
    FLASK_ENV = 'testing'
    DEBUG = False
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
