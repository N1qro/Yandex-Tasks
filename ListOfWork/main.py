import os.path
from flask import Flask, render_template, flash, redirect, url_for
from data import db_session
from data.users import User
from datetime import datetime
from forms import RegistrationForm

app = Flask(__name__)
app.secret_key = "super-secret-key"


@app.route("/")
def homepage():
    return render_template("homepage.html", redirect="/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        newEntry = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
            modified_date=datetime.now()
        )

        newEntry.set_password(form.password.data)
        db_sess.add(newEntry)
        db_sess.commit()

        flash("Успешная регистрация!")
        return redirect(url_for("register"))

    return render_template("register.html",
                           title="Регистрация",
                           form=form)


if __name__ == "__main__":
    db_session.global_init(os.path.join("db", "db.db"))
    app.run(host="127.0.0.1", port=8080, debug=True)
