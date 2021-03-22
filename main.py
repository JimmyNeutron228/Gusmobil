from data import db_session
from data.users import Users
from data.ads import Ads
from data.favorites import Favorites
from forms.login import LoginForm
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def entrance():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.is_remember_me.data)
            return redirect("/")
        return render_template('entrance.html',
                               message='Wrong login or password',
                               form=form)
    return render_template('entrance.html', title='Login', form=form)


if __name__ == '__main__':
    main()
