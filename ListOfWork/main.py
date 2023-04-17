import os.path
from flask import Flask, render_template
from data import db_session
from data.jobs import Job
from data.users import User

app = Flask(__name__)
app.secret_key = "super-secret-key"


@app.route("/")
def homepage():
    db_sess = db_session.create_session()
    jobs_query = db_sess.query(Job, User).join(User).all()

    return render_template("worklog.html",
                           title="Журнал работы",
                           data=jobs_query)


if __name__ == "__main__":
    db_session.global_init(os.path.join("db", "db.db"))
    app.run(host="127.0.0.1", port=8080, debug=True)
