from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/training/<string:prof>")
@app.route("/training")
def index(prof=None):
    kind = None
    if (prof is not None and ("инженер" in prof.lower() or "строитель" in prof.lower())):
        kind = "Инженерные тренажёры"
    elif prof is not None:
        kind = "Научные симуляторы"

    return render_template("base.html", kind=kind)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
