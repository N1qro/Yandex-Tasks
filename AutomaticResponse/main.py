import json
from flask import Flask, render_template
app = Flask(__name__)

with open("form_data.json", encoding="UTF-8") as jsonFile:
    data = json.load(jsonFile)


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/answer")
@app.route("/auto_answer")
def answer():
    return render_template(
        template_name_or_list="auto_answer.html",
        data=data["answers"],
        scheme=data["scheme"]
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
