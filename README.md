## chapter 1 :   A "Hello, World" Flask Application

```
from flask import Flask
app = Flask(__name__)  #creating instanse of class flask which we import
from app import routes # import routes  

```
* create routes 
```
from app import app

@app.route('/')
def index():
return 'Hello world'
```
###useful commands:
`pip install flask`

`export FLASK_APP=file.py ` to set the main file to run

`flask run` -> run development server


##Chapter 2: Templates
 * To activate the env : `source venv/bin/activate`
and `deactivate ` to exit .
<br>
 * we can send any data with decorator i.e `  user = {'user_name': 'Hamza'}`
 * and use {{}} to inject it in html page.
 * we use `return render_template('index.html', user=user, posts=posts)  ` to render template.
 *  <b>if statement syntax <b>
 ```
 {% if something%}
    do it 
 {% else %}
    do another
 {% endif %}
 ```
    
* <b>for loop statement syntax <b>
 ```
 {% for some in somes%}
    {{some}}

 {% endfor %}
 ```
* create templates folder and inside it `base.html ` which holds the base content for others pages.
`{%  block content %} {% endblock %}` refers to the dynamic data.
* 

## Chapter 3 :Introduction to Flask-WTF 


*To handle the web forms in this application , we use the Flask-WTF extension, which is a thin wrapper around the WTForms package that nicely integrates it with Flask.
`$ pip install flask-wtf`

 * to use this extension and protect web forms from attack:

 * add secret_key in init file as a dictionary :

 ` app.config['secret key'] = '1fdbsfsdjfhdsfusd'`
 or we can made class in seperate file "config.py" in main directory.



`class Config(object):
    secret_key = os.environ.get('secret_key') or 'foodstuffs'`
`
    
## user login form :

* create forms.py in app 
* create class LoginField as follows:
```
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,validators
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    remember_me = BooleanField('Remember me ')
    submit = SubmitField('sign in ')



```

* create a html template :
``` 
<form action="" method="post">
    {{form.hidden_tag() }} #to protect data [SECRET KEY]
    <p> {{form.username.lable }}</p> <br>
      {{form.username(size=32)}}
  <p>{{form.password.label}}</p> <br>
        {{form.password()}} `
    `{{form.hidden_tag() }}`
```
* create a route for login as follows , create instance of class 
```
from app.forms import LoginForm

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='sign in ', form=form)

```

* if we want to send flash message after submitting thr form 
```
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login successful for {form.username.data}')
        return redirect('/')
    return render_template('login.html', title='sign in ', form=form)
```

* and in base file 
```
{% with messages = get_flashed_messages () %}
{% if messages %}
<ul>
    {% for msg in messages %}
    <li> {{msg}}</li>
    {% endfor %}
    </ul>
{% endif %}}
{% endwith %}
```
hgfhfghg

* To make the route dynamaic :  we use 

`  <a href="{{ url_for('index') }}">Home</a> `

and with redirect 
`redirect(url_for('index'))`


# Chapter 4 : DataBase# micro_blog
