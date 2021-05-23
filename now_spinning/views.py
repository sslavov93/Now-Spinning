from now_spinning import app

from flask import render_template


@app.route('/')
def hello():
    return render_template("index.html", title="Time To Say Goodbye", artist="Envio", year="2004")
