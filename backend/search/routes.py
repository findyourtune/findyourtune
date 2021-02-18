import os
from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, session, current_app
from flask_session import Session
from flask_wtf import Form
from flask_jwt_extended import jwt_required
from wtforms.fields.html5 import DateField
import jwt
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from backend import db
from backend.music.utils import get_track_obj
from backend.models import Users
from backend.auth.utils import session_cache_path, is_users_spotify_linked

search = Blueprint('search', __name__)

@search.route("/api/search/search_users/<search_string>", methods=['GET'])
def search_users(search_string):
    # ilike is case insensitive
    users = Users.query.filter(Users.username.ilike('%' + search_string + '%') | 
                               Users.firstname.ilike('%' + search_string + '%') | 
                               Users.lastname.ilike('%' + search_string + '%') 
                              )
    print( users )
    results = []
    for user in users:
        user_dict = {
            'username': user.username,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'spotify_account': user.spotify_account,
            ''
        }
        results.append(user_dict)
    return( jsonify(results) )