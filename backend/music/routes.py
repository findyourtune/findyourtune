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


music = Blueprint('music', __name__)


@music.route("/api/music/get_music/<username>", methods=['GET'])
@jwt_required
def get_music(username):
    spotify_linked = is_users_spotify_linked(username)
    if spotify_linked:
        user = Users.query.filter_by(username=username).first()
        cache_file = user.spotify_account
        auth_manager = spotipy.oauth2.SpotifyOAuth( client_id=current_app.config['SPOTIFY_CLIENT_ID'], 
                                                    client_secret=current_app.config['SPOTIFY_SECRET_ID'],
                                                    redirect_uri=current_app.config['SPOTIFY_REDIRECT_URI'],
                                                    show_dialog=False,
                                                    cache_path=session_cache_path(cache_file),
                                                    scope=current_app.config['SCOPE'] )


        cache_token = auth_manager.get_access_token()
        access_token = cache_token['access_token']
        spotify_object = spotipy.Spotify(access_token)

        top_tracks_s = spotify_object.current_user_top_tracks(limit='20', time_range="short_term")
        top_tracks_s_list = []
        for track in top_tracks_s['items']:
            top_tracks_s_list.append(get_track_obj(track))

        return jsonify(top_tracks_s_list), 200
    else:
        return jsonify(), 200