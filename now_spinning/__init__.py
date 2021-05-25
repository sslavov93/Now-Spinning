from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, instance_relative_config=True)
config_map = {
    "production": "config.ProductionConfig",
    "development": "config.DevelopmentConfig",
    "testing": "config.TestingConfig"
}
app.config.from_object(config_map.get(app.config["ENV"], "config.DevelopmentConfig"))


db = SQLAlchemy(app)

with app.app_context():
    from now_spinning import views

if __name__ == '__main__':
    app.run()
