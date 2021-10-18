from os import environ
from flask import Flask, request, render_template
import bot
import psycopg2

app = Flask(__name__)

if __name__ == "__main__":
  app.run(environ.get('PORT'), debug=True)

# Database connection
# db = sqlite3.connect('sunsets.db', check_same_thread=False)
# cur = db.cursor()

db = environ.get("DATABASE_URL")
conn = psycopg2.connect(db)
cur = conn.cursor()

@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "POST":
      bot.start()
      cur.execute("SELECT time, location, image, text FROM tweets ORDER BY time DESC;")
      tweets = cur.fetchall()
      return render_template("index.html", tweets=tweets)
  else:
      # Perform database selection
      cur.execute("SELECT time, location, image, text FROM tweets ORDER BY time DESC;")
      tweets = cur.fetchall()
      return render_template("index.html", tweets=tweets)
