from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("index.html", title="Time To Say Goodbye", artist="Envio", year="2004")
