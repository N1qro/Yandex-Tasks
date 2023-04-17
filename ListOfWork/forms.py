from flask_wtf import FlaskForm
from wtforms import (IntegerField, PasswordField,
                     StringField, SubmitField)
from wtforms.validators import (InputRequired, Length, EqualTo,
                                NumberRange, Email)


class RegistrationForm(FlaskForm):
    email = StringField("Login / email", validators=[
        InputRequired("Логин или почта не заполнены"),
        Email("Формат почты не соблюден")
    ])

    password = PasswordField("Password", validators=[
        InputRequired("Пароль не заполнен"),
        Length(min=8, message="Длина пароля от 8 символов")
    ])

    password_repeat = PasswordField("Password", validators=[
        InputRequired("Повторите пароль"),
        EqualTo("password", "Пароли не совпадают")
    ])

    surname = StringField("Surname", validators=[
        InputRequired("Не введена фамилия"),
        Length(max=50, message="Слишком длинная фамилия. Мы вам не рады")
    ])

    name = StringField("Name", validators=[
        InputRequired("Не введено имя"),
        Length(max=50, message="Слишком длинное имя. Мы вам не рады")
    ])

    age = IntegerField("Age", validators=[
        InputRequired("Укажите возраст"),
        NumberRange(0, 100, "Недействительный возраст")
    ])

    position = StringField("Position", validators=[
        InputRequired("Укажите должность")
    ])

    speciality = StringField("Speciality", validators=[
        InputRequired("Укажите специальность")
    ])

    address = StringField("Address", validators=[
        InputRequired("Укажите адрес вашего модуля")
    ])

    submit = SubmitField("Submit")