from os import environ
from flask import Flask, render_template

app = Flask(__name__)
app.run(environ.get('PORT'))

@app.route("/")
def index():
    return render_template("index.html")