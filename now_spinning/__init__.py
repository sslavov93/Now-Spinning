from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

# TODO Fix this (create a make command / fab task to prepopulate the DB
from now_spinning.models import Track
db.drop_all()
db.create_all()
db.session.add(Track(title="Time To Say Goodbye (Original Mix)", artist="Envio", year="2004"))
db.session.commit()

with app.app_context():
    from now_spinning import views
