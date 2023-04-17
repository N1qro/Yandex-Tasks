from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "super-secret-key"


@app.route("/")
def homepage():
    return render_template("homepage.html", redirect="/carousel")


@app.route("/carousel")
def showcase():
    files = ["mars1.jpg", "mars2.jpeg", "mars3.jpg"]

    return render_template("carousel.html",
                           title="Пейзажи марса",
                           files=files)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
