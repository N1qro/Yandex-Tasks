from flask import Flask, render_template
from functools import lru_cache
from planets import Database
app = Flask(__name__)


@lru_cache(1)
def get_available_planets():
    return ', '.join(Database.keys())


@lru_cache(len(Database.keys()))
def get_planet_description(planet):
    return Database[planet]


@app.route("/")
@app.route("/index")
def home_index():
    return """
        <body>
            <h2>Домашняя страница</h2>
            <a href="choice/Марс">Перейти на решение задачи</a>
        </body>
    """


@app.route("/choice/<string:planet_name>")
def planet_index(planet_name: str):
    capitalized_name = planet_name.capitalize()
    if capitalized_name in Database:
        return render_template(
            template_name_or_list="index.html",
            planet_name=capitalized_name,
            descriptions=get_planet_description(capitalized_name)
        )
    else:
        return render_template(
            template_name_or_list="default.html",
            planet_name=capitalized_name,
            available_planets=get_available_planets()
        )



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
