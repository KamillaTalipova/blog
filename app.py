from flask import Flask, render_template, url_for, redirect
from data import db_session
from data.user import User
from data.registerForm import RegisterForm
from data.loginForm import LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required
db_session.global_init("db/blogs.sqlite")

app=Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',message="Неправильный логин или пароль",form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if len(form.password.data)<6:
            return render_template('register.html', title='Регистрация',form=form,message="Пароль слишком короткий")
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',form=form,message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',form=form,message="Такой пользователь уже есть")
        user = User(name=form.name.data,email=form.email.data,about=form.about.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/store')
def store():
    return render_template('store.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/store/principal')
def principal():
    return render_template('principal.html')


@app.route('/store/stress')
def stress():
    return render_template('stress.html')


@app.route('/store/buy')
def buy():
    return render_template('buy.html')


if __name__=='__main__':
    app.run(debug=True)