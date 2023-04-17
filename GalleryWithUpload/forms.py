from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField
from wtforms.validators import InputRequired


class FileUploadForm(FlaskForm):
    image_file = FileField("Загрузите изображение", validators=[
        InputRequired()
    ])
    submit = SubmitField("Отправить")
