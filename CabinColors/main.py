from flask import Flask, render_template, abort
app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("homepage.html", redirect="/table_param/male/99")


@app.route("/table_param/<gender>/<age>")
def table(gender, age):
    try:
        assert gender in ("male", "female")
        assert 0 < int(age) < 100
    except (AssertionError, ValueError):
        abort(404)
    else:
        hue = round((int(age) / 99) * 360)
        return render_template(
            "cabin_color.html",
            title="Оформление каюты",
            sex=gender,
            age=int(age),
            hue=hue
        )
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
