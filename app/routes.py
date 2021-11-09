from flask.helpers import url_for
from flask.templating import render_template
from app.forms import LoginForm
from flask import flash,redirect
from app import app


@app.route('/index')
@app.route('/')
def index():
    user = {'user_name': 'Hamza'}
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
    return render_template('index.html', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login successful for {form.username.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='sign in ', form=form)
