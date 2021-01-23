import os
from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, session, current_app
from flask_session import Session
from flask_wtf import Form
from flask_jwt_extended import jwt_required
from wtforms.fields.html5 import DateField
import spotipy
import uuid


main = Blueprint('main', __name__)

SCOPE = 'user-library-read user-read-playback-position'

COURSES = [
    {
        'title': 'Effective JavaScript: 68 Specific Ways to Harness the Power of JavaScript ',
        'author': 'David Herman',
        'paperback': True
    },
    {
        'title': 'JavaScript: The Good Parts',
        'author': 'Douglas Crockford',
        'paperback': False    
    },
    {
        'title': 'Eloquent JavaScript: A Modern Introduction to Programming',
        'author': 'Marijn Haverbeke',
        'paperback': True
    }
] 

@main.route("/")
def home():
    return 'Hello World'

@main.route("/api/testapi", methods=['GET'])
@jwt_required
def testapi():
    return jsonify({
        'status': 'success',
        'courses': COURSES
    })

def session_cache_path():
    return './.spotify_caches/' + session.get('uuid')

@main.route("/link_spotify", methods=['GET', 'POST'])
def link_spotify():
    if not session.get('uuid'):
        session['uuid'] = str(uuid.uuid4())
    
    auth_manager = spotipy.oauth2.SpotifyOAuth( client_id=current_app.config['SPOTIFY_CLIENT_ID'], 
                                                client_secret=current_app.config['SPOTIFY_SECRET_ID'],
                                                redirect_uri=current_app.config['SPOTIFY_REDIRECT_URI'],
                                                cache_path=session_cache_path(),
                                                show_dialog=True,
                                                scope=SCOPE )
    
    if request.args.get('code'):
        auth_manager.get_access_token(request.args.get("code"))
        redirect('/link_spotify')
    
    if not auth_manager.get_cached_token():
        auth_url = auth_manager.get_authorize_url()
        return jsonify({
            'auth_url': auth_url
        })

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()

