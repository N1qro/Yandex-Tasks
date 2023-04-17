from data import db_session
from data.users import User
from datetime import datetime
from wtforms.validators import StopValidation


def UserExistValidator():

    def validator(_, field):
        db = db_session.create_session()
        user = db.query(User).filter(User.id == field.data).first()

        if not user:
            raise StopValidation(f"Пользователь с ID {field.data} не был найден")

    return validator


def DateTimeValidator(format):
    def validator(form, field):
        try:
            datetime.strptime(field.data, format)
        except ValueError:
            raise StopValidation("Формат времени и даты не соблюден")

    return validator


def CollaboratorsValidator():
    COLLABORATOR_NOT_FOUND = "Коллаборатора с ID {} не существует"
    BAD_FORMAT = "В коллабораторах есть буквы, не только цифры."

    def validator(form, field):
        if not field.data:
            return

        try:
            collaborators = set(map(int, field.data.split(",")))
        except ValueError:
            raise StopValidation(BAD_FORMAT)
        db = db_session.create_session()
        users = db.query(User).filter(User.id.in_(collaborators)).all()

        uids = set(user.id for user in users)
        missing = collaborators.difference(uids)
        print(uids)
        print(collaborators)
        print(missing)

        if missing:
            raise StopValidation(COLLABORATOR_NOT_FOUND.format(missing.pop()))

    return validator


def EmailExistsValidator(shouldExist=False):
    EMAIL_EXISTS = "Эта почта уже зарегистрирована"
    EMAIL_INVALID = "Такой почты не существует. Сначала зарегистрируйте её"

    def validator(_, field):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == field.data).first()

        if shouldExist and not user:
            raise StopValidation(EMAIL_INVALID)
        if not shouldExist and user:
            raise StopValidation(EMAIL_EXISTS)

        return True

    return validator
