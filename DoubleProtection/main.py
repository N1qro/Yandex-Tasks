from flask import Flask, render_template, flash, redirect, url_for

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class ProtectionForm(FlaskForm):
    astronautId = StringField("ID астронавта", validators=[DataRequired()])
    astronautPassword = PasswordField("Пароль астронавта", validators=[DataRequired()])
    captainId = StringField("ID капитана", validators=[DataRequired()])
    captainPassword = PasswordField("Пароль капитана", validators=[DataRequired()])
    submitButton = SubmitField("Доступ")


@app.route("/")
def homepage():
    return render_template("homepage.html", redirect="/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = ProtectionForm()
    if form.validate_on_submit():
        flash("Успешный логин!")
        return redirect(url_for("homepage"))        
    return render_template("login.html", title="Авторизация", form=form)
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
