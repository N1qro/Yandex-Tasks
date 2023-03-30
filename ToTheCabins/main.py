import json
from flask import Flask, render_template, flash, redirect, url_for
app = Flask(__name__)

with open("cabin_data.json", encoding="UTF-8") as jsonFile:
    data = json.load(jsonFile)

@app.route("/")
def homepage():
    return render_template("homepage.html", redirect="/distribution")


@app.route("/distribution")
def login(): 
    return render_template("distribution.html", title="Распределение", data=data)
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
