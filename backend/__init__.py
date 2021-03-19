from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from backend.config import Config

import os


db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
mail = Mail()
bootstrap = Bootstrap()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(Config)

    api = Api(app)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    jwt.init_app(app)


    # Used to blacklist inactive jwt tokens, not being used right now as log out 
    # function is just deleting jwt token from localStorage
    blacklist = set()
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist

    from backend.search.routes import search
    from backend.social.routes import social
    from backend.auth.routes import auth
    from backend.music.routes import music
    from backend.errors.handlers import errors
    from backend.suggested.routes import suggested  
    
    app.register_blueprint(search)
    app.register_blueprint(social)   
    app.register_blueprint(auth)
    app.register_blueprint(music)
    app.register_blueprint(errors) 
    app.register_blueprint(suggested)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    with app.app_context():
        from backend.models import Users # Import the models
        db.create_all()  # Create sql tables for our data models

        # Check if admin user exists, if not, create it
        user = Users.query.filter_by(username=app.config['ADMIN_USER_USERNAME']).first()
        if user == None:
            hashed_password = bcrypt.generate_password_hash(app.config['ADMIN_USER_PASSWORD']).decode('utf-8')
            admin_user = Users(username=app.config['ADMIN_USER_USERNAME'], email=app.config['ADMIN_USER_EMAIL'], password=hashed_password, firstname=app.config['ADMIN_USER_FIRSTNAME'], lastname=app.config['ADMIN_USER_LASTNAME'])
            db.session.add(admin_user)
            db.session.commit()
            print('Admin user created!')

    caches_folder = './.spotify_caches/'
    if not os.path.exists(caches_folder):
        os.makedirs(caches_folder)

    return app