import os
from flask import Flask, request, render_template
import psycopg2
import bot
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database connection
db = os.getenv("DATABASE_URL")
conn = psycopg2.connect(db)
cur = conn.cursor()
# Perform database selection
cur.execute("SELECT time, location, image, text, id FROM tweets ORDER BY time DESC;")
tweets = cur.fetchall()
conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
  return render_template("index.html", tweets=tweets)