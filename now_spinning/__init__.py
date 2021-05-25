from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.DevConfig')

db = SQLAlchemy(app)

with app.app_context():
    from now_spinning import views

if __name__ == '__main__':
    app.run()
