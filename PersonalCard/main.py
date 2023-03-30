import json
import os.path

from random import choice
from flask import Flask, render_template

app = Flask(__name__)
with open(os.path.join("templates", "personnel.json"), encoding="UTF-8") as jsonFile:
    data = json.load(jsonFile)


@app.route("/")
def homepage():
    return render_template("homepage.html", redirect="/member")


@app.route("/member")
def login():
    return render_template("personal_card.html", title="Личная карточка", data=choice(data))
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
