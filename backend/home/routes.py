from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_wtf import Form
from wtforms.fields.html5 import DateField
from backend import db
# from backend.models import User
# from flask_login import current_user
# from datetime import datetime, date

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return 'Hello World'