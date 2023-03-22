import json
from flask import Flask, render_template
app = Flask(__name__)

with open("professions.json", encoding="UTF-8") as jsonFile:
    professions = json.load(jsonFile)


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/list_prof/<string:list_type>")
def index(list_type):
    return render_template(
        "base.html",
        type=list_type,
        professions=professions, 
        error=list_type not in ("ol", "ul")
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
