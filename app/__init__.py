from flask import Flask
from config import Config
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'gfdkgndfogndgio'
from app import routes

app.config.from_object(Config)