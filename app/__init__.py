from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)

db= SQLAlchemy(app)
migrate=Migrate(app , db)

# app.config['SECRET_KEY'] = 'gfdkgndfogndgio'
from app import routes , models

app.config.from_object(Config)