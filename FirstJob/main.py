import os.path
from datetime import datetime
from flask import Flask
from data import db_session
from data.jobs import Job

app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"


if __name__ == "__main__":
    db_session.global_init(os.path.join("db", "db.db"))
    db_sess = db_session.create_session()

    newJob = Job()
    newJob.team_leader = 1
    newJob.job = "deployment of residential modules 1 and 2"
    newJob.work_size = 15
    newJob.collaborators = "2, 3"
    newJob.start_date = datetime.now()
    newJob.is_finished = False

    db_sess.add(newJob)
    db_sess.commit()
    db_sess.close()
    # app.run(host="127.0.0.1", port=8080)
