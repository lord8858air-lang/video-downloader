from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    character = {
        "name": "Xiao Yan",
        "novel": "Battle Through the Heavens",
        "age": "15 → 30+",
        "cultivation": [
            ("Dou Zhi", "Chapter 1"),
            ("Dou Shi", "Chapter 120"),
            ("Dou Wang", "Chapter 450"),
            ("Dou Zun", "Chapter 900"),
            ("Dou Di", "Final Arc")
        ],
        "donghua": {
            "season": "BTTH",
            "breakthrough_episode": "Season 4 Episode 24"
        }
    }
    return render_template("index.html", character=character)

if __name__ == "__main__":
    app.run()
