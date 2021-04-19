from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class Adds(FlaskForm):
    brand = StringField('Марка', validators=[DataRequired()])
    model = StringField('Модель', validators=[DataRequired()])
    price = IntegerField('Цена, ₽', validators=[DataRequired()])
    transmission = SelectField('КПП', choices=[('Механическая', 'Механическая'),
                                                ('Автоматическая', "Автоматическая"),
                                                ('Роботизированная', "Роботизированная"),
                                                ('Вариаторная КПП', "Вариаторная КПП")],
                               validators=[DataRequired()])
    engine = SelectField('Двигатель', choices=[('Бензиновый', 'Бензиновый'),
                                               ('Дизельный', "Дизельный"),
                                               ('Электрические', "Электрические")],
                               validators=[DataRequired()])
    steering_wheel = SelectField('Руль', choices=[('Левый', 'Левый'), ('Правый', "Правый")], validators=[DataRequired()])
    power = IntegerField('Мощность (Л.С.)', validators=[DataRequired()])
    drive_unit = SelectField('Привод', choices=[('Передний', 'Передний'),
                                               ('Задний', "Задний"),
                                               ('Полный', "Полный")],
                               validators=[DataRequired()])
    mileage = IntegerField('Пробег', validators=[DataRequired()])
    year = IntegerField('Год выпуска', validators=[DataRequired()])
    about = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField('Добавить объявление')