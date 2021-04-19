from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class EditProfileForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField("Электронная почта", validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    password = PasswordField('Текущий пароль', validators=[DataRequired()])
    submit = SubmitField('Изменить')