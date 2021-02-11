from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, abort, Response, current_app
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from backend import db, bcrypt
from backend.models import Users, UsersSchema
from backend.auth.forms import (RegistrationForm, LoginForm,
                                   RequestResetForm, ResetPasswordForm)
from backend.auth.utils import save_picture, send_reset_email, validate_register, validate_login, validate_profile_edit
from backend.errors.handlers import InvalidAPIUsage
from flask_restful import Resource, Api, reqparse
import os
import datetime
import jwt
import spotipy


auth = Blueprint('auth', __name__)

@auth.route("/api/auth/register", methods=['GET', 'POST'])
def register():
    data = request.json
    users_schema = UsersSchema()
    validate_register(data)
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = Users(username=data['username'], email=data['email'], password=hashed_password, firstname=data['firstname'], lastname=data['lastname'])
    db.session.add(user)
    db.session.commit()
    return jsonify(users_schema.dump(user)), 200


@auth.route("/api/auth/login", methods=['GET', 'POST'])
def login():
    data = request.json
    validate_login(data)
    user = Users.query.filter_by(email=data['email']).first()
    try:
        authorized = bcrypt.check_password_hash(user.password, data['password'])
        if not authorized:
            raise InvalidAPIUsage('Login unsuccessful', status_code=410) # Incorrect password
    except:
        raise InvalidAPIUsage('Login unsuccessful', status_code=410) # Incorrect email
    
    expires = datetime.timedelta(days=7)
    users_schema = UsersSchema()
    ret = {
        'access_token': create_access_token(identity=users_schema.dump(user), expires_delta=expires), # access_tokens identity contains entire user info from table
        'refresh_token': create_refresh_token(identity=users_schema.dump(user), expires_delta=expires), # refresh_tokens identity contains entire user info from table
        'email': user.email,
        'username': user.username,
        'user_id': user.user_id,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'appcolor': user.appcolor,
        'spotify_account': user.spotify_account
    }
    return jsonify(ret), 200


# Standard refresh endpoint. A blacklisted refresh token
# will not be able to access this endpoint
@auth.route('/api/auth/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


# Endpoint for revoking the current users access token
@auth.route('/api/auth/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


# Endpoint for revoking the current users refresh token
@auth.route('/api/auth/logout2', methods=['DELETE'])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


# This will now prevent users with blacklisted tokens from
# accessing this endpoint
@auth.route('/api/auth/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify({'hello': 'world'})


@auth.route("/api/auth/get_user_info", methods=['GET'])
@jwt_required
def getUserInfo():
    data = request
    users_schema = UsersSchema()
    # Code takes jwt token from request params
    token = request.args.get("access_token")

    # Code takes jwt token from request header
    # token = request.headers['Authorization']
    # token2 = token.split(' ')
    # headerToken = token2[1]

    decoded = jwt.decode(token, verify=False)
    # print(decoded['identity'])
    user = Users.query.filter_by(username=decoded['identity']['username']).first()

    return jsonify({
        'status': 'success',
        'userInfo': users_schema.dump(user)
    }), 200


@auth.route("/api/auth/reset_password", methods=['GET', 'POST'])
def reset_request():
    data = request.json
    user = Users.query.filter_by(email=data['email']).first()
    send_reset_email(user)

    return jsonify({
        'status': 'success'
    }), 200


@auth.route("/api/auth/reset_password_token", methods=['GET', 'POST'])
def reset_token():
    data = request.json
    user = Users.verify_reset_token(data['token'])
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user.password = hashed_password
    db.session.commit()

    return jsonify({
        'status': 'success'
    }), 200


@auth.route("/api/auth/update_profile", methods=['GET', 'POST'])
@jwt_required
def update_profile():
    data = request.json
    validate_profile_edit(data)
    token = request.headers['Authorization']
    token2 = token.split(' ')
    header_token = token2[1]
    decoded = jwt.decode(header_token, verify=False)
    user = Users.query.filter_by(username=decoded['identity']['username']).first()
    user.firstname = data['firstname']
    user.lastname = data['lastname']
    user.username = data['username']
    user.email = data['email']
    db.session.commit()
    
    expires = datetime.timedelta(days=7)
    users_schema = UsersSchema()
    ret = {
        'access_token': create_access_token(identity=users_schema.dump(user), expires_delta=expires), # access_tokens identity contains entire user info from table
        'refresh_token': create_refresh_token(identity=users_schema.dump(user), expires_delta=expires), # refresh_tokens identity contains entire user info from table
        'email': user.email,
        'username': user.username,
        'user_id': user.user_id,
        'firstname': user.firstname,
        'lastname': user.lastname
    }
    return jsonify(ret), 200

@auth.route("/api/auth/update_appcolor", methods=['GET', 'POST'])
@jwt_required
def update_appcolor():
    data = request.json
    token = request.headers['Authorization']
    token2 = token.split(' ')
    header_token = token2[1]
    decoded = jwt.decode(header_token, verify=False)
    user = Users.query.filter_by(username=decoded['identity']['username']).first()
    user.appcolor = data['appcolor']
    db.session.commit()
    
    expires = datetime.timedelta(days=7)
    users_schema = UsersSchema()
    ret = {
        'access_token': create_access_token(identity=users_schema.dump(user), expires_delta=expires), # access_tokens identity contains entire user info from table
        'refresh_token': create_refresh_token(identity=users_schema.dump(user), expires_delta=expires), # refresh_tokens identity contains entire user info from table
        'email': user.email,
        'username': user.username,
        'user_id': user.user_id,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'appcolor': user.appcolor
    }
    return jsonify(ret), 200

def session_cache_path(cache_file):
    return './.spotify_caches/' + cache_file

@auth.route("/api/auth/link_spotify", methods=['GET', 'POST'])
@jwt_required
def link_spotify():
    data = request.json
    token = request.headers['Authorization']
    token2 = token.split(' ')
    header_token = token2[1]
    decoded = jwt.decode(header_token, verify=False)
    user = Users.query.filter_by(username=decoded['identity']['username']).first()
    user.spotify_account = data['spotify_account']
    db.session.commit()
    
    expires = datetime.timedelta(days=7)
    users_schema = UsersSchema()
    cache_file = str(data['spotify_account'])
    auth_manager = spotipy.oauth2.SpotifyOAuth( client_id=current_app.config['SPOTIFY_CLIENT_ID'], 
                                                client_secret=current_app.config['SPOTIFY_SECRET_ID'],
                                                redirect_uri=current_app.config['SPOTIFY_REDIRECT_URI'],
                                                show_dialog=True,
                                                cache_path=session_cache_path(cache_file),
                                                scope=current_app.config['SCOPE'] )
    auth_url = None
    if not auth_manager.get_cached_token():
        auth_url = auth_manager.get_authorize_url()

    ret = {
        'access_token': create_access_token(identity=users_schema.dump(user), expires_delta=expires), # access_tokens identity contains entire user info from table
        'refresh_token': create_refresh_token(identity=users_schema.dump(user), expires_delta=expires), # refresh_tokens identity contains entire user info from table
        'email': user.email,
        'username': user.username,
        'user_id': user.user_id,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'appcolor': user.appcolor,
        'auth_url': auth_url,
        'spotify_account': user.spotify_account
    }
    return jsonify(ret), 200

@auth.route("/api/auth/link_spotify_callback", methods=['GET', 'POST'])
def link_spotify_callback():
    cache_file = 'temp'
    auth_manager = spotipy.oauth2.SpotifyOAuth( client_id=current_app.config['SPOTIFY_CLIENT_ID'], 
                                                client_secret=current_app.config['SPOTIFY_SECRET_ID'],
                                                redirect_uri=current_app.config['SPOTIFY_REDIRECT_URI'],
                                                show_dialog=True,
                                                cache_path=session_cache_path(cache_file),
                                                scope=current_app.config['SCOPE'] )

    if request.args.get('code'):
        auth_manager.get_access_token(request.args.get("code"))
        redirect('/api/auth/link_spotify_callback')
    
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    sp_user = spotify.current_user()
    from_file = open(session_cache_path(cache_file), 'r')
    to_file = open(session_cache_path(str(sp_user['id'])), 'w')
    to_file.write(from_file.read())
    to_file.close()
    from_file.close()
    os.remove(session_cache_path(cache_file))
    return redirect(current_app.config['FRONTEND_URL'] + '/#/profile')