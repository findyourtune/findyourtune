import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from backend import mail, db
from backend.models import Users, Spotify_Account_Token
from backend.errors.handlers import InvalidAPIUsage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import path
import smtplib
import jwt
import json


def get_user_info_from_token(request):
    try:
        token = request.headers['Authorization']
        token2 = token.split(' ')
        
        if token2 and len(token2) > 1:
            headerToken = token2[1]
            decoded = jwt.decode(headerToken, verify=False)
            return decoded['identity']
        else:
            return None
    except:
        return None


def session_cache_path(cache_file):
    path = './.spotify_caches/' + cache_file
    if os.path.isfile(path):
        return path
    token = Spotify_Account_Token.query.filter_by(user_account=cache_file).first()
    if token != None:
        json_str = '{"access_token":"' + token.access_token + '","token_type":"' + token.token_type + '","expires_in":' + token.expires_in + ',"scope":"' + token.scope + '","expires_at":' + token.expires_at + ',"refresh_token":"' + token.refresh_token + '"}'
        print(json_str)
        f = open(path, 'w')
        f.write(json_str)
        f.close()
    return path

def is_users_spotify_linked(username):
    user = Users.query.filter_by(username=username).first()

    user_spotify_account = user.spotify_account
    if user_spotify_account:
        cache_directory = session_cache_path(user_spotify_account)
        spotify_cache_file_exists = path.exists(cache_directory)
        spotify_linked = True if spotify_cache_file_exists and user_spotify_account is not None else False
        return spotify_linked
    else:
        return False

def db_write_spotify_token(token, user):
    token = json.loads(token)
    spotify_account_token = Spotify_Account_Token(access_token=token['access_token'],
                                                  token_type=token['token_type'], 
                                                  expires_in=token['expires_in'],
                                                  scope=token['scope'],
                                                  expires_at=token['expires_at'],
                                                  refresh_token=token['refresh_token'],
                                                  user_account=user)
    db.session.add(spotify_account_token)
    db.session.commit()

# Not yet implemented
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'assets', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    # FROM = os.environ['EMAIL_USER']
    FROM = os.environ['EMAIL_USER_SD']
    TO = user.email
    token = user.get_reset_token()
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Password Reset for Find Your Tune"
    msg['From'] = FROM
    msg['To'] = TO
    text = f'''To reset your password, visit the following link:
    http://localhost:8081/?#/resetPasswordToken/''' + token 
    '''

    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    print(text)
    part1 = MIMEText(text, 'plain')
    msg.attach(part1)

    server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server_ssl.ehlo() # optional, called by login()
    server_ssl.login(os.environ['EMAIL_USER_SD'], os.environ['EMAIL_PASS_SD'])  
    server_ssl.sendmail(FROM, TO, msg.as_string())
    server_ssl.close()


def validate_register(data):
    if data['firstname'] == '':
        raise InvalidAPIUsage('Please provide a first name', status_code=410)
    
    if data['lastname'] == '':
        raise InvalidAPIUsage('Please provide a last name', status_code=410)

    if data['username'] == '':
        raise InvalidAPIUsage('Please provide a username', status_code=410)

    if data['email'] == '':
        raise InvalidAPIUsage('Please provide a valid email', status_code=410)

    if data['password'] == '':
        raise InvalidAPIUsage('Please enter a password', status_code=410)

    user = Users.query.filter_by(username=data['username']).first()
    if user:
        raise InvalidAPIUsage('That username is taken. Please choose a different one.', status_code=410)

    user = Users.query.filter_by(email=data['email']).first()
    if user:
        raise InvalidAPIUsage('That email is taken. Please choose a different one.', status_code=410)
    
    if data['password'] != data['confirmPassword']:
        raise InvalidAPIUsage('Passwords must match.', status_code=410)


def validate_login(data):
    if data['email'] == '':
        raise InvalidAPIUsage('Please provide a valid email', status_code=410)

    if data['password'] == '':
        raise InvalidAPIUsage('Please enter a password', status_code=410)


def validate_profile_edit(data):
    if data['firstname'] == '':
        raise InvalidAPIUsage('Please provide a first name', status_code=410)
    
    if data['lastname'] == '':
        raise InvalidAPIUsage('Please provide a last name', status_code=410)

    if data['username'] == '':
        raise InvalidAPIUsage('Please provide a username', status_code=410)

    if data['email'] == '':
        raise InvalidAPIUsage('Please provide a valid email', status_code=410)