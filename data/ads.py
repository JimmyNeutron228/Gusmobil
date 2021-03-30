import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Ads(SqlAlchemyBase):
    __tablename__ = 'ads'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    brand = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    model = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    transmission = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    engine = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    steering_wheel = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    power = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    drive_unit = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    mileage = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    images = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user = orm.relation('Users')

    favorites = orm.relation('Favorites', back_populates='ad')
