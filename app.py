
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    characters = [
        {
            "name": "Xiao Yan",
            "novel": "Battle Through the Heavens",
            "power": "Dou Sheng",
            "breakthrough": "Chapter 1648",
            "age": "24",
            "manhwa": "Chapter 385",
            "donghua": "Season 5"
        }
    ]
    return render_template("index.html", characters=characters)

if __name__ == "__main__":
    app.run()
