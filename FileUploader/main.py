import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join("static", "img")
app.secret_key = "ASLJKdnkdfjkladfklNFSJKdf;a;dfksadkfL:Asd,.xzc,c,xz.cx.z,aASQWe"


@app.route("/")
def homepage_view():
    return render_template("homepage.html")


@app.route("/load_photo", methods=["GET", "POST"])
def fileuploader_view():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return render_template("fileuploader.html", filename=os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return render_template("fileuploader.html", filename=None)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
