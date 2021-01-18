from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from backend.config import Config

import os


db = SQLAlchemy()
# bcrypt = Bcrypt()
# login_manager = LoginManager()
# login_manager.login_view = 'users.login'
# login_manager.login_message_category = 'info'
# mail = Mail()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(Config)

    api = Api(app)

    ma = Marshmallow(app)

    db.init_app(app)


    from backend.home.routes import main
    from backend.errors.handlers import errors    
    
    app.register_blueprint(main)   
    app.register_blueprint(errors) 

    with app.app_context():
        from backend import models  # Import the models
        db.create_all()  # Create sql tables for our data models

        return app

    return app