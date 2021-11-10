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
create the migration repository/directory for microblog by running `flask db init`

* to create the first database migration, which will include the users table that maps to the User database model. `flask db migrate -m "anycomment"` .
* The flask db migrate command does not make any changes to the database, it just generates the migration script. To apply the changes to the database, the `flask db upgrade` command must be used.
* Note that Flask-SQLAlchemy uses a "snake case" naming convention for database tables by default. For the User model above, the corresponding table in the database will be named user. For a AddressAndPhone model class, the table would be named address_and_phone.

###  Database Upgrade and Downgrade Workflow
* `flask db downgrade`  --> which undoes the last migration.
* `flask db histroy`  --> show the history of migration
* `flask db current ` --> show the current migration .


###  Database Relationships 

* Relational databases are good at storing relations between data items. Consider the case of a user writing a blog post. The user will have a record in the users table, and the post will have a record in the posts table. The most efficient way to record who wrote a given post is to link the two related records.
```
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
```

* `posts = db.relationship('Post', backref='author', lazy='dynamic')`.
* db.relationship :  high-level view of the relationship between users and posts, and for that reason it isn't in the database diagram. For a one-to-many relationship, a db.relationship field is normally defined on the "one" side, and is used as a convenient way to get access to the "many".
* backref argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object.
* lazy argument defines how the database query for the relationship will be issued.
* "Post" is the class where we want to which holds the foreign key. 


### playing with database
```
>>> u = User(username='john', email='john@example.com') -> creating rows in user table
>>> db.session.add(u)
>>> db.session.commit()  -> commit changes
>>> users = User.query.all() -> to get all data in table
>>> users
```

## Chapter 5 :Password Hashing
* One of the packages that implement password hashing is Werkzeug.
* The whole password hashing logic can be implemented as two new methods in the user model:


```
from werkzeug.security import generate_password_hash, check_password_hash

# ...

class User(db.Model):
    # ...

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```


 ### Introduction to Flask-Login
* Flask-Login. This extension manages the user logged-in state, so that for example users can log in to the application and then navigate to different pages while the application "remembers" that the user is logged in. It also provides the "remember me" functionality that allows users to remain logged in even after closing the browser window.
`$ pip install flask-login`
* ask-Login needs to be created and initialized right after the application instance in app/__init__.py. This is how this extension is initialized:
```
# ...
from flask_login import LoginManager

app = Flask(__name__)
# ...
login = LoginManager(app)
```
### user mixin
* Flask-login requires a User model with the following properties:

* has an is_authenticated() method that returns True if the user has provided valid credentials

* has an is_active() method that returns True if the user’s account is active

* has an is_anonymous() method that returns True if the current user is an anonymous user <br>
* has a get_id() method which, given a User instance, returns the unique ID for that object <br>

UserMixin class provides the implementation of this properties. Its the reason you can call for example is_authenticated to check if login credentials provide is correct or not instead of having to write a method to do that yourself. <br>
* Flask-Login provides a mixin class called UserMixin that includes generic implementations that are appropriate for most user model classes. Here is how the mixin class is added to the model:
```
# ...
from flask_login import UserMixin

class User(UserMixin, db.Model):
    # ...
```

###   User Loader Function
* Because Flask-Login knows nothing about databases, it needs the application's help in loading a user. For that reason, the extension expects that the application will configure a user loader function, that can be called to load a user given the ID. This function can be added in the app/models.py module:
```
from app import login
# ...

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
   ##an argument is going to be a string, so databases that use numeric IDs need to convert the string to integer 
```
### Logging Users In
filter by: 

For this purpose I'm using the filter_by() method of the SQLAlchemy query object. The result of filter_by() is a query that only includes the objects that have a matching username. Since I know there is only going to be one or zero results, I complete the query by calling first(), which will return the user object if it exists, or None

```
app/routes.py: Login view function logic
# ...
from flask_login import current_user, login_user
from app.models import User

# ...

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

```

The top two lines in the login() function deal with a weird situation. Imagine you have a user that is logged in, and the user navigates to the /login URL of your application. Clearly that is a mistake, so I want to not allow that. The current_user variable comes from Flask-Login and can be used at any time during the handling to obtain the user object that represents the client of the request. The value of this variable can be a user object from the database (which Flask-Login reads through the user loader callback I provided above), or a special anonymous user object if the user did not log in yet. Remember those properties that Flask-Login required in the user object? One of those was is_authenticated, which comes in handy to check if the user is logged in or not. When the user is already logged in, I just redirect to the index page.

In place of the flash() call that I used earlier, now I can log the user in for real. The first step is to load the user from the database. The username came with the form submission, so I can query the database with that to find the user. For this purpose I'm using the filter_by() method of the SQLAlchemy query object. The result of filter_by() is a query that only includes the objects that have a matching username. Since I know there is only going to be one or zero results, I complete the query by calling first(), which will return the user object if it exists, or None if it does not. In Chapter 4 you have seen that when you call the all() method in a query, the query executes and you get a list of all the results that match that query. The first() method is another commonly used way to execute a query, when you only need to have one result.

If I got a match for the username that was provided, I can next check if the password that also came with the form is valid. This is done by invoking the check_password() method I defined above. This will take the password hash stored with the user and determine if the password entered in the form matches the hash or not. So now I have two possible error conditions: the username can be invalid, or the password can be incorrect for the user. In either of those cases, I flash an message, and redirect back to the login prompt so that the user can try again.

If the username and password are both correct, then I call the login_user() function, which comes from Flask-Login. This function will register the user as logged in, so that means that any future pages the user navigates to will have the current_user variable set to that user.

To complete the login process, I just redirect the newly logged-in user to the index page.

###  Logging Users Out

```
app/routes.py: Logout view function
# ...
from flask_login import logout_user

# ...

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
```
```
#edit the base.html to change the sign in to sign out

  {% if current_user.is_anonymous %}
        <a href="{{ url_for('login') }}">Login</a>
    {% else %}
    <a href="{{ url_for('logout') }}">logout</a>

    {% endif %}
```
  ## Requiring Users to Login

If a user who is not logged in tries to view a protected page, Flask-Login will automatically redirect the user to the login form, and only redirect back to the page the user wanted to view after the login process is complete.


```
app/__init__.py:

# ...
login = LoginManager(app)
login.login_view = 'login'

in routes.py:
@login_required
def index():
 ...
```


* To handle visiting the page which user want to visit if hasn't sign in
```
app/routes.py: Redirect to "next" page
from flask import request
from werkzeug.urls import url_parse

@app.route('/login', methods=['GET', 'POST'])
def login():
    # ...
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

```

*Right after the user is logged in by calling Flask-Login's login_user() function, the value of the next query string argument is obtained. Flask provides a request variable that contains all the information that the client sent with the request. In particular, the request.args attribute exposes the contents of the query string in a friendly dictionary format. There are actually three possible cases that need to be considered to determine where to redirect after a successful login:

If the login URL does not have a next argument, then the user is redirected to the index page.
If the login URL includes a next argument that is set to a relative path (or in other words, a URL without the domain portion), then the user is redirected to that URL.
If the login URL includes a next argument that is set to a full URL that includes a domain name, then the user is redirected to the index page.
The first and second cases are self-explanatory. The third case is in place to make the application more secure. An attacker could insert a URL to a malicious site in the next argument, so the application only redirects when the URL is relative, which ensures that the redirect stays within the same site as the application. To determine if the URL is relative or absolute, I parse it with Werkzeug's url_parse() function and then check if the netloc component is set or not.


### User Registration
<a href="https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins"> link User Registration </a>

`pip install email-validator
`
```

app/forms.py: User registration form
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

# ...

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    
    ## To make sure that the username and email address entered by the user are not already in the database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
```

## Chapter 6: Profile Page and Avatars:
<a href="https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vi-profile-page-and-avatars"> Profile Page and Avatars </a>

## Chapter 7: Error Handling
  * Sending Errors by Email

<a href="https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling"> Chapter 7: Error Handling</a>

` export FLASK_DEBUG=1 `

## Chapter 8 :   Database Relationships Revisited

* one to many 
<img src="https://blog.miguelgrinberg.com/static/images/mega-tutorial/ch04-users-posts.png" > 


  * <b> Many-to-Many </b> 

consider a database that has students and teachers. I can say that a student has many teachers, and a teacher has many students. It's like two overlapped one-to-many relationships from both ends.
<img src="https://blog.miguelgrinberg.com/static/images/mega-tutorial/ch08-students-teachers.png" > 

* Many-to-One and One-to-One

A many-to-one is similar to a one-to-many relationship. The difference is that this relationship is looked at from the "many" side.

A one-to-one relationship is a special case of a one-to-many. The representation is similar, but a constraint is added to the database to prevent the "many" side to have more than one link. While there are cases in which this type of relationship is useful, it isn't as common as the other types.

* A **self-referential relationship** in which instances of a class are linked to other instances of the same class is called a self-referential relationship , i.e users following each other.