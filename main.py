import os
from data import db_session
from data.users import Users
from data.ads import Ads
from data.favorites import Favorites
from forms.login import LoginForm
from forms.ads import Adds
from forms.register import RegisterForm
from forms.edit_profile import EditProfileForm
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


@app.route('/favorite')
def favorite():
    print(2)
    if current_user.is_authenticated:
        print(1)
        session = db_session.create_session()
        fav = session.query(Favorites).filter(Favorites.user_id == current_user.id).all()
        adds = []
        for elem in fav:
            adds.append(session.query(Ads).filter(Ads.id == elem.ad_id).first())
        return render_template('favorite.html', favorites=adds)
    return abort(404)


@app.route('/add_to_favorite/<int:id>')
@login_required
def add_to_favorites(id):
    db_sess = db_session.create_session()
    add = db_sess.query(Ads).filter(Ads.id == id).first()
    favorite_add = Favorites(
        ad_id=id,
        user_id=current_user.id
    )
    db_sess.add(favorite_add)
    db_sess.commit()
    return redirect('/')


@app.route('/del_to_favorite/<int:id>')
@login_required
def del_to_favorites(id):
    db_sess = db_session.create_session()
    add = db_sess.query(Favorites).filter(Favorites.ad_id == id).first()
    db_sess.delete(add)
    db_sess.commit()
    return redirect('/')


@app.route('/add/<int:id>')
def add(id):
    session = db_session.create_session()
    add = session.query(Ads).filter(Ads.id == id).first()
    count = len(os.listdir(add.images))
    return render_template('add.html', count=count, add=add)


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
    db_sess = db_session.create_session()
    ads = db_sess.query(Ads).all()
    if current_user.is_authenticated:
        favorite = db_sess.query(Favorites).filter(Favorites.user_id == current_user.id).all()
        return render_template('index.html', ads=ads, favorite=favorite)
    return render_template('index.html', ads=ads)


@app.route('/add_ad', methods=['GET', 'POST'])
@login_required
def add_ads():
    form = Adds()
    if form.validate_on_submit():
        session = db_session.create_session()
        add = Ads(
            brand=form.brand.data,
            model=form.model.data,
            price=form.price.data,
            transmission=form.transmission.data,
            engine=form.engine.data,
            steering_wheel=form.steering_wheel.data,
            power=form.power.data,
            drive_unit=form.drive_unit.data,
            mileage=form.mileage.data,
            year=form.year.data,
            about=form.about.data
        )
        requested_files = request.files.getlist('file')
        id = session.query(Users).filter(Users.name == current_user.name,
                                         Users.email == current_user.email,
                                         Users.surname == current_user.surname).first().id
        os.chdir(f'static/users_data/profile_{id}')
        dir_kol = len(os.listdir())
        os.mkdir(f'ad_{dir_kol + 1}')
        os.chdir(f'ad_{dir_kol + 1}')
        for i in range(len(requested_files)):
            requested_files[i].save(f'image_{i + 1}.jpg')
        db_images_dir = os.getcwd().replace('\\', '/')
        db_images_dir = db_images_dir[db_images_dir.index('users_data'):]
        add.images = 'static/' + db_images_dir
        add.user_id = id
        session.add(add)
        session.commit()
        os.chdir('../../../..')
        return redirect('/')
    return render_template('add_ad.html', form=form)


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
                               message='Неверный логин или пароль!',
                               form=form)
    return render_template('entrance.html', title='Вход', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("register.html", form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(Users).filter(Users.email == form.email.data).first():
            return render_template("register.html", title="Регистрация", form=form,
                                   message="Такой пользователь уже есть")
        user = Users(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        id = session.query(Users).filter(Users.name == user.name,
                                         Users.email == user.email,
                                         Users.surname == user.surname).first().id
        os.chdir('static/users_data')
        new_dir_name = 'profile_' + str(id)
        if not os.path.isdir(new_dir_name):
            os.mkdir(new_dir_name)
        os.chdir('../..')
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/profile')
def profile():
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.email == current_user.email).first()
    return render_template('profile.html', title='Личный кабинет')


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.email == current_user.email).first()
        if user:
            form.name.data = user.name
            form.surname.data = user.surname
            form.email.data = user.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.email == current_user.email).first()
        if user and user.check_password(form.password.data):
            user.name = form.name.data
            user.surname = form.surname.data
            user.email = form.email.data
            db_sess.merge(user)
            db_sess.commit()
            return redirect('/profile')
        return render_template("edit_profile.html", title="Редактирование профиля", form=form,
                               message="Неверный пароль")
    return render_template('edit_profile.html', form=form, title='Редактирование профиля')


if __name__ == '__main__':
    main()
