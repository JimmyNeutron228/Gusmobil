import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Favorites(SqlAlchemyBase):
    __tablename__ = 'favorites'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    ad_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('ads.id'))

    user = orm.relation('Users')
    ad = orm.relation('Ads')
