import os.path
from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"


users = [
    ["Scott", "Ridley", 21, "captain", "research engineer", "module_1", "scott_chief@mars.org"],
    ["Andrew", "Novikov", 17, "team-lead", "programmer", "module_2", "andrey777-novikov777@yandex.ru"],
    ["Egor", "Tomchuk", 19, "best friend", "finances", "module_3", "someemail@certainly.exists"]
]


if __name__ == "__main__":
    db_session.global_init(os.path.join("db", "db.db"))
    db_sess = db_session.create_session()

    for user in users:
        newUser = User()
        newUser.surname = user[0]
        newUser.name = user[1]
        newUser.age = user[2]
        newUser.position = user[3]
        newUser.speciality = user[4]
        newUser.address = user[5]
        newUser.email = user[6]
        db_sess.add(newUser)

    db_sess.commit()
    db_sess.close()
    # app.run(host="127.0.0.1", port=8080)
