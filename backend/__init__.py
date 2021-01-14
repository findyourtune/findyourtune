from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from backend.config import Config


db = SQLAlchemy()
# bcrypt = Bcrypt()
# login_manager = LoginManager()
# login_manager.login_view = 'users.login'
# login_manager.login_message_category = 'info'
# mail = Mail()
bootstrap = Bootstrap()

#test


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from backend.home.routes import main
    app.register_blueprint(main)

    return app