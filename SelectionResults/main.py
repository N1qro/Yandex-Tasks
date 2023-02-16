from flask import Flask, render_template
app = Flask(__name__)

SUCCESSFUL_COMPLETION_RATING_AMOUNT = 40


@app.route('/results/<string:username>/<int:level>/<float:rating>')
def results_view(username, level, rating):
    if rating > 100:
        return None

    return render_template(
        template_name_or_list="resultpage.html",
        username=username,
        level=level,
        rating=rating,
        next_selection=level + 1,
        passed = rating > SUCCESSFUL_COMPLETION_RATING_AMOUNT
    )


@app.route('/')
def homepage_view():
    return render_template("homepage.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)