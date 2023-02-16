from flask import Flask, render_template
app = Flask(__name__)


@app.route('/astronaut_selection')
def form_view():
    return render_template("base.html")

@app.route('/')
def index_view():
    return "<body>Это базовая страница. Решение находится на /astronaut_selection</body>"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')