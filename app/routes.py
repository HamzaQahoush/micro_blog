from flask.templating import render_template
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from flask import flash, redirect, request, url_for, request
from app.models import User
from werkzeug.urls import url_parse


@app.route('/index')
@app.route('/')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'john'},
            'body': 'beautiful day in portland'
        },
        {
            'author': {'username': 'Hamza'},
            'body': 'beautiful day in Liwwa'
        },

    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data).first()  # take username from form and search my database if we find user object.
        # flash(f'Login successful for {form.username.data}')
        if user is None or not user.check_password(form.password.data):
            flash('invalid user name or password')
            return redirect(url_for('login'))
        login_user(user,
                   remember=form.remember_me.data)  # in case the sign in successed , store the user id in sesssion
        next_page = request.args.get('next')
        if not next_page or not next_page.startwith('/'):
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='sign in ', form=form)


# clear user session
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulation , You are now registered user ')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)
