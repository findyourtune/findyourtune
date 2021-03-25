import os
from os.path import join, dirname
from dotenv import load_dotenv


class Config:
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '.env'))
    load_dotenv(dotenv_path)


    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_SECRET_KEY = os.getenv( 'JWT_SECRET_KEY' )
    FRONTEND_URL = os.getenv( 'FRONTEND_URL' )
    SCOPE = os.getenv( 'SCOPE' )
    SECRET_KEY = os.getenv( 'SECRET_KEY' )
    SESSION_TYPE = os.getenv( 'SESSION_TYPE' )
    SESSION_FILE_DIR = os.getenv( 'SESSION_FILE_DIR' )
    SPOTIFY_CLIENT_ID = os.getenv( 'SPOTIFY_CLIENT_ID' )
    SPOTIFY_SECRET_ID = os.getenv( 'SPOTIFY_SECRET_ID' )
    SPOTIFY_REDIRECT_URI = os.getenv( 'SPOTIFY_REDIRECT_URI' )
    SQLALCHEMY_DATABASE_URI = os.getenv( 'SQLALCHEMY_DATABASE_URI' )
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = os.getenv( 'CORS_HEADERS' )

    ADMIN_USER_USERNAME = os.getenv( 'ADMIN_USER_USERNAME' )
    ADMIN_USER_FIRSTNAME = os.getenv( 'ADMIN_USER_FIRSTNAME' )
    ADMIN_USER_LASTNAME = os.getenv( 'ADMIN_USER_LASTNAME' )
    ADMIN_USER_EMAIL = os.getenv( 'ADMIN_USER_EMAIL' )
    ADMIN_USER_PASSWORD = os.getenv( 'ADMIN_USER_PASSWORD' )