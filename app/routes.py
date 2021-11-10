from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from flask import flash, redirect, request, url_for, render_template
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()


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
        if not next_page or url_parse(next_page).netloc != '':
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


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title="edit profile", form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()  # get the username
    if not user:
        flash(f'User {username} Not found ')
        return redirect(url_for('index'))
    if user == current_user:
        flash('You can not follow your self')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash (f'You are following {username}')
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()  # get the username
    if not user:
        flash(f'User {username} Not found ')
        return redirect(url_for('index'))
    if user == current_user:
        flash('You can not unfollow your self')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash (f'You are unfollowing {username}')
    return redirect(url_for('user', username=username))
