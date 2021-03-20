from data import db_session
from data.users import Users
from data.ads import Ads
from data.favorites import Favorites
from flask import Flask, request, abort
from flask import render_template, redirect
from flask_login import LoginManager, login_user
from flask_login import login_required, logout_user, current_user


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'ISBN5-89392-055-4'


def main():
    db_session.global_init('db/gus_auto.db')
    app.run()


@app.route('/')
def index():
    return ''


if __name__ == '__main__':
    main()
