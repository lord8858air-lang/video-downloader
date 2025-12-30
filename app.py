
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 Your Render Flask App is Working!"

# ⚠️ DO NOT use app.run() on Render
