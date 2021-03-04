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
from backend.models import Users, Follow_Relationship
from sqlalchemy.orm import aliased

suggested = Blueprint('suggested', __name__)

@suggested.route("/api/suggested/get_suggested_people/<username>", methods=['GET'])
@jwt_required
def get_suggested_people(username):
    if Users.query.filter_by(username=username).first() is None:
        return jsonify({"msg": "User does not exist."}), 500
    user1 = aliased(Users)
    user2 = aliased(Users)
    suggested_following = []
    my_following_relationships = db.session.query(user1.username.label('u_username'), user2.username.label('f_username'), user2.firstname.label('f_firstname'), user2.lastname.label('f_lastname'), user2.appcolor.label('f_appColor'), Follow_Relationship)\
                                        .join(Follow_Relationship, (Follow_Relationship.follower_id == user1.user_id))\
                                        .join(user2, user2.user_id == Follow_Relationship.followed_id)\
                                        .filter(user1.username == username)\
                                        .order_by(Follow_Relationship.timestamp.desc()).all()
    my_all_following_relationships = [{
        'user_username': relationship.f_username,
        'user_firstname': relationship.f_firstname,
        'user_lastname': relationship.f_lastname,
        'user_appcolor': relationship.f_appColor,
        'timestamp': relationship.Follow_Relationship.timestamp,
        'user_followed': True
        } for relationship in my_following_relationships]

    for i in my_all_following_relationships:
        following_username = i['user_username']
        following_user_following_relationships = db.session.query(user1.username.label('u_username'), user2.username.label('f_username'), user2.firstname.label('f_firstname'), user2.lastname.label('f_lastname'), user2.appcolor.label('f_appColor'), Follow_Relationship)\
                                            .join(Follow_Relationship, (Follow_Relationship.follower_id == user1.user_id))\
                                            .join(user2, user2.user_id == Follow_Relationship.followed_id)\
                                            .filter(user1.username == following_username)\
                                            .order_by(Follow_Relationship.timestamp.desc()).all()
        following_user_all_following_relationships = [{
        'user_username': relationship.f_username,
        'user_firstname': relationship.f_firstname,
        'user_lastname': relationship.f_lastname,
        'user_appcolor': relationship.f_appColor,
        'timestamp': relationship.Follow_Relationship.timestamp,
        'user_followed': True
        } for relationship in following_user_following_relationships]

        if len(following_user_all_following_relationships) > 0:
            current_suggested_len = len(suggested_following)
            while len(suggested_following) != current_suggested_len + 1:
                for j in following_user_all_following_relationships:
                    suggested_following.append(j)
    print({'people': suggested_following})
    return jsonify({'people': suggested_following})