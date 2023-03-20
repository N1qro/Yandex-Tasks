from flask import Flask, render_template
app = Flask(__name__)


@app.route("/index/<string:title>")
def index(title):
    return render_template("base.html", title=title)


@app.route("/<string:title>")
def index2(title):
    return render_template("base.html", title=title)


@app.route("/")
def index3():
    return render_template("base.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
