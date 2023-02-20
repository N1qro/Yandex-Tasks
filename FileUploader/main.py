from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def homepage_view():
    return render_template("homepage.html")


@app.route("/load_photo")
def fileuploader_view():
    return render_template("fileuploader.html")



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
