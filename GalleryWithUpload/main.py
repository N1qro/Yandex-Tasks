import os
from flask import Flask, render_template, redirect
from forms import FileUploadForm
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "super-secret-key"


@app.route("/")
def homepage():
    return render_template("homepage.html", redirect="/carousel")


@app.route("/carousel", methods=["GET", "POST"])
def showcase():
    form = FileUploadForm()
    if form.validate_on_submit():
        new_filename = secure_filename(form.image_file.data.filename)
        form.image_file.data.save(os.path.join("static", new_filename))
        return redirect("/carousel")
    else:
        files = [os.path.basename(f) for f in os.listdir("static")]
        return render_template("carousel.html",
                               title="Пейзажи марса",
                               files=files,
                               form=form)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
