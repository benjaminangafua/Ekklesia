
from os import path
import os
from flask import Flask
from cs50 import SQL

db = SQL('sqlite:///church.db')

# db = SQL(os.getenv("DATABASE_URL"))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aglkghhfklahlhggakhfg'

    # Initialize database
    
    from .views import views
    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')  
    return app

