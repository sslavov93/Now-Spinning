import os
import json
import sys

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


def configure(app):
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS

    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    with open(f'{application_path}/config.json') as f:
        config = json.load(f)
    app.config.update(config)


def create_app():
    # if getattr(sys, 'frozen', False):
    #     application_path = sys._MEIPASS
    #     template_folder = os.path.join(application_path, 'templates')
    #     static_folder = os.path.join(application_path, 'static')
    #     app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    # else:
    #     application_path = os.path.dirname(os.path.abspath(__file__))
    #     app = Flask(__name__)
    #
    # print("da eba maika ti")
    # print(application_path)
    #
    # with open(f'{application_path}/config.json') as f:
    #     config = json.load(f)
    # app.config.update(config)

    app = Flask(__name__)
    app.config.from_object("config.DevelopmentConfig")
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        from now_spinning import views

    return app
