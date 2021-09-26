from os import environ
from flask import Flask, request, redirect, render_template
import bot
import time

app = Flask(__name__)

if __name__ == "__main__":
  app.run(environ.get('PORT'), debug=True)
    
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        bot.start()
        images = bot.loadimage()
        return render_template("index.html", images=images)
    else:
        images = bot.loadimage()
        return render_template("index.html", images=images)

