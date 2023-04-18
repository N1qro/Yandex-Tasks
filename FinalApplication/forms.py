from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import (PasswordField, StringField, SubmitField,
                     EmailField, IntegerField, DateTimeField,
                     BooleanField)
from wtforms.validators import (InputRequired, EqualTo, Email, Length,
                                NumberRange)
from validators import (EmailExistsValidator, CollaboratorsValidator,
                        UserExistValidator, DateTimeValidator)


class RegisterForm(FlaskForm):
    email = StringField("Почта", validators=[
        InputRequired("Почта не указана"),
        Email("Формат почты не соблюден")
    ])

    password = PasswordField("Пароль", validators=[
        InputRequired("Пароль не заполнен"),
        Length(min=8, message="Длина пароля от 8 символов")
    ])

    password_repeat = PasswordField("Повторите пароль", validators=[
        InputRequired("Повторите пароль"),
        EqualTo("password", "Пароли не совпадают")
    ])

    surname = StringField("Фамилия", validators=[
        InputRequired("Не введена фамилия"),
        Length(max=50, message="Слишком длинная фамилия. Мы вам не рады")
    ])

    name = StringField("Имя", validators=[
        InputRequired("Не введено имя"),
        Length(max=50, message="Слишком длинное имя. Мы вам не рады")
    ])

    age = IntegerField("Возраст", validators=[
        InputRequired("Укажите возраст"),
        NumberRange(0, 100, "Недействительный возраст")
    ])

    position = StringField("Должность", validators=[
        InputRequired("Укажите должность")
    ])

    speciality = StringField("Специальность", validators=[
        InputRequired("Укажите специальность")
    ])

    address = StringField("Адрес модуля", validators=[
        InputRequired("Укажите адрес вашего модуля")
    ])

    submit = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):
    email = EmailField("Почта", validators=[
        InputRequired("Email не заполнен"),
        EmailExistsValidator(shouldExist=True)
    ])
    password = PasswordField("Пароль", validators=[
        InputRequired("Пароль не заполнен")
    ])
    submit = SubmitField("Войти")


class WorkForm(FlaskForm):
    job_name = StringField("Название работы", validators=[
        InputRequired("Введите название работы")
    ])

    job_leader = IntegerField("ID главы работы", validators=[
        UserExistValidator()
    ])

    work_hours = IntegerField("Сколько часов потребуется на эту работу",
                              validators=[
                                InputRequired("Рабочие часы не указаны"),
                                NumberRange(
                                    min=0,
                                    message="Рабочие часы не могут быть <0")
                              ])

    collaborators = StringField("ID помощников (через запятую)", validators=[
        CollaboratorsValidator()
    ])

    start_date = StringField("Время начала работ",
                             validators=[DateTimeValidator("%Y-%m-%d %H:%M:%S")],
                             default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    work_finished = BooleanField("Работа уже завершена?")
    finish_date = StringField("Время конца работ",
                              validators=[DateTimeValidator("%Y-%m-%d %H:%M:%S")],
                              default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    submit = SubmitField("Добавить")
