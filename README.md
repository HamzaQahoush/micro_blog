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

* To make the route dynamaic :  we use 

`  <a href="{{ url_for('index') }}">Home</a> `

and with redirect 
`redirect(url_for('index'))`


# Chapter 4 : DataBase# micro_blog
### Flask-SQLAlchemy Configuration

* To use database we need to install package `pip install flask-sqlalchemy`
* sqlalchemy support relational database , mysql , postgres ,
*then we need to install ` pip install flask-migrate`This extension is a Flask wrapper for Alembic, a database migration framework for SQLAlchemy.
* to tell flask sqlalchemy location and type of database , we use config variable.
`SQLALCHMY_DATABASE_URI = "sqlite:///app.db"` 
* OR to generate absoulte path name for the db file :
` basedir = os.path.abspath(os.path.dirname(__file__))`
```
class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```
* The SQLALCHEMY_TRACK_MODIFICATIONS configuration option is set to False to disable a feature of Flask-SQLAlchemy that I do not need, which is to send a signal to the application every time a change is about to be made in the database.

* `in __init__ file `:
```
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db= SQLAlchemy(app) #creete an instance of 
migrate=Migrate(app , db)

#then we need to create model.py and import it .
from app import routes,models

```

### Database Models
* The data that will be stored in the database will be represented by a collection of classes, usually called database models.
* Object–relational mapping (ORM, O/RM, and O/R mapping tool) in computer science is a programming technique for converting data between incompatible type systems using object-oriented programming languages.
* The ORM layer within SQLAlchemy will do the translations required to map objects created from these classes into rows in the proper database tables.
```

from app import db


class User(db.Model):
    # dbModel  base class for database models provided by SQLalchamy
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f"User {self.username}"
"""
The __repr__ method tells Python how to print objects of this class, which is going to be useful for debugging
"""
```

### Creating the Migration Repository

* to make changes to that structure such as adding new things, and sometimes to modify or remove items. Alembic (the migration framework used by Flask-Migrate) will make these schema changes in a way that does not require the database to be recreated from scratch every time a change needs to be made.
create the migration repository for microblog by running `flask db init`