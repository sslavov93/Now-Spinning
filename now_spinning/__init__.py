from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    config_map = {
        "production": "config.ProductionConfig",
        "development": "config.DevelopmentConfig",
        "testing": "config.TestingConfig",
    }
    app.config.from_object(config_map.get(app.config.get("ENV"), "config.DevelopmentConfig"))
    db.init_app(app)

    migrate.init_app(app, db)

    with app.app_context():
        from now_spinning import views

    return app
