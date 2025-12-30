
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            message = f"URL received successfully ✅"
        else:
            message = "Please enter a valid URL ❌"
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run()
