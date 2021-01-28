import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from backend import mail
from backend.models import Users
from backend.errors.handlers import InvalidAPIUsage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os


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


# First server side validation function. May want a dedicated file for server side form validation...
def validate_register(data):
    if data['firstname'] == '':
        raise InvalidAPIUsage('Please provide a first name', status_code=410)
    
    if data['lastname'] == '':
        raise InvalidAPIUsage('Please provide a last name', status_code=410)

    user = Users.query.filter_by(username=data['username']).first()
    if user:
        raise InvalidAPIUsage('That username is taken. Please choose a different one.', status_code=410)

    user = Users.query.filter_by(email=data['email']).first()
    if user:
        raise InvalidAPIUsage('That email is taken. Please choose a different one.', status_code=410)
    
    if data['password'] != data['confirmPassword']:
        raise InvalidAPIUsage('Passwords must match.', status_code=410)
    