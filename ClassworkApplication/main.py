import os.path
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user
from forms import LoginForm, RegisterForm, WorkForm
from datetime import datetime
from data import db_session
from data.users import User
from data.jobs import Job


app = Flask(__name__)
app.secret_key = "super-secret-key"

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def homepage():
    db_sess = db_session.create_session()
    jobs_query = db_sess.query(Job, User).join(User).all()

    return render_template("worklog.html",
                           title="Журнал работы",
                           data=jobs_query)


@app.route("/add-new-work", methods=["GET", "POST"])
@login_required
def workappender():
    form = WorkForm()
    if form.validate_on_submit():
        newEntry = Job(
            team_leader=form.job_leader.data,
            job=form.job_name.data,
            work_size=form.work_hours.data,
            collaborators=form.collaborators.data,
            start_date=datetime.strptime(form.start_date.data, "%Y-%m-%d %H:%M:%S"),
            end_date=datetime.strptime(form.finish_date.data, "%Y-%m-%d %H:%M:%S"),
            is_finished=form.work_finished.data
        )

        db = db_session.create_session()
        db.add(newEntry)
        db.commit()

        return redirect(url_for("homepage"))

    most_recent_error = None
    if form.errors:
        most_recent_error = tuple(form.errors.values())[0][-1]

    print(form.errors)
    return render_template("workadder.html",
                           error=most_recent_error,
                           form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db = db_session.create_session()
        user = db.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("homepage"))

        return render_template("login.html",
                               form=form,
                               error="Неправильный логин или пароль")

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
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
        )

        newEntry.set_password(form.password.data)
        db_sess.add(newEntry)
        db_sess.commit()

        login_user(newEntry)
        flash("Успешная регистрация!")
        return redirect(url_for("homepage"))

    return render_template("register.html",
                           title="Регистрация",
                           form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


if __name__ == "__main__":
    db_session.global_init(os.path.join("db", "db.db"))
    app.run(host="127.0.0.1", port=8000, debug=True)
