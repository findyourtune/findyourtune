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
from backend.music.utils import get_track_obj, get_playlist_obj, get_album_obj
from backend.models import Users
from backend.auth.utils import session_cache_path, is_users_spotify_linked, get_user_info_from_token

search = Blueprint('search', __name__)

@search.route("/api/search/search_users/<search_string>", methods=['GET'])
def search_users(search_string):
    try :
        current_user = get_user_info_from_token(request)

        current_username = current_user['username']
        current_user = Users.query.filter_by(username=current_username).first()
    except:
        pass

    # ilike is case insensitive
    users = Users.query.filter(Users.username.ilike('%' + search_string + '%') | 
                               Users.firstname.ilike('%' + search_string + '%') | 
                               Users.lastname.ilike('%' + search_string + '%') 
                              )
    user_results = []
    for user in users:
        user_dict = {
            'username': user.username,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'spotify_account': user.spotify_account
        }
        user_results.append(user_dict)

    searched_tracks_list = []
    if current_user:
        spotify_linked = is_users_spotify_linked(current_user.username)
        if spotify_linked:
            user = Users.query.filter_by(username=current_user.username).first()
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

            # searched_tracks = spotify_object.current_user_top_tracks(q=search_string, type='track,album,playlist', limit='20')
            searched_tracks = spotify_object.search(q=search_string, type='track', limit='25')
            for track in searched_tracks['tracks']['items']:
                searched_tracks_list.append(get_track_obj(track))

    results = {
        'users': user_results,
        'music': searched_tracks_list
    }
    return( jsonify(results) )


@search.route("/api/search/get_spotify_embed/<search_string>", methods=['GET'])
@jwt_required
def get_spotify_embed(search_string):
    current_user = get_user_info_from_token(request)

    if current_user is not None:
        current_username = current_user['username']
    else:
        current_username = None

    spotify_linked = is_users_spotify_linked(current_username)
    searched_tracks_list = []
    searched_playlists_list = []
    searched_albums_list = []
    if spotify_linked:
        user = Users.query.filter_by(username=current_username).first()
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

        searched_tracks = spotify_object.search(q=search_string, type='track', limit='20')
        for track in searched_tracks['tracks']['items']:
            searched_tracks_list.append(get_track_obj(track))

        searched_albums = spotify_object.search(q=search_string, type='album', limit='20')
        for album in searched_albums['albums']['items']:
            searched_albums_list.append(get_album_obj(album))

        searched_playlists = spotify_object.search(q=search_string, type='playlist', limit='20')
        for playlist in searched_playlists['playlists']['items']:
            searched_playlists_list.append(get_playlist_obj(playlist))
        
        rtn = {
            'songs': searched_tracks_list,
            'albums': searched_albums_list,
            'playlists': searched_playlists_list
        }
        return jsonify(rtn), 200
    else:
        return jsonify([]), 200