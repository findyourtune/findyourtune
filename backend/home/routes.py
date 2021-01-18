from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_wtf import Form
from wtforms.fields.html5 import DateField
from backend import db
# from backend.models import User
# from flask_login import current_user
# from datetime import datetime, date

main = Blueprint('main', __name__)

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

@main.route("/testapi", methods=['GET'])
def testapi():
    return jsonify({
        'status': 'success',
        'courses': COURSES
    })