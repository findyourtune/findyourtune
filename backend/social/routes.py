import os
from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, session, current_app
from flask_session import Session
from flask_wtf import Form
from flask_jwt_extended import jwt_required
from wtforms.fields.html5 import DateField
import uuid
from backend import db

from backend.models import Users, Posts, Comments, Likes, Direct_Messages, Follow_Requests, Follow_Relationship

social = Blueprint('social', __name__)

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

@social.route("/")
def home():
    return 'Hello World'

@social.route("/api/testapi", methods=['GET'])
@jwt_required
def testapi():
    return jsonify({
        'status': 'success',
        'courses': COURSES
    })

@social.route("/api/social/post", methods=['POST'])
@jwt_required
def post():
    data = request.json

    if Users.query.filter_by(username=data['username']).first() is None:
        return jsonify({"msg": "User does not exist."}), 500

    post_user_id = Users.query.filter_by(username=data['username']).first()

    post = Posts(user_id=post_user_id.user_id, text=data['text'], spotify_data=data['spotify_data'])
    db.session.add(post)
    db.session.commit()
    return jsonify({"msg": "Post created."}), 201


@social.route("/api/social/get_posts", methods=['GET'])
def get_posts():
    posts = Posts.query.order_by(Posts.timestamp.desc()).all()

    all_posts = [{
        'post_id': post.post_id, 
        'user_id': post.user_id, 
        'name': Users.query.filter_by(user_id = post.user_id).first().firstname + " " + Users.query.filter_by(user_id = post.user_id).first().lastname,
        'text': post.text, 
        'spotify_data': post.spotify_data, 
        'timestamp': post.timestamp
        } for post in posts]

    return jsonify(all_posts), 200

@social.route("/api/social/get_posts/<username>", methods=['GET'])
def get_posts_user(username):
    # posts = Posts.query.join(Users, Users.user_id == Posts.user_id).filter_by(user_id = Users.username).order_by(Posts.timestamp.desc()).all()
    posts = db.session.query(Posts).join(Users, Users.user_id == Posts.user_id).filter(Users.username == username).order_by(Posts.timestamp.desc()).all()

    all_posts = [{
        'post_id': post.post_id, 
        'user_id': post.user_id, 
        'name': Users.query.filter_by(user_id = post.user_id).first().firstname + " " + Users.query.filter_by(user_id = post.user_id).first().lastname,
        'text': post.text, 
        'spotify_data': post.spotify_data, 
        'timestamp': post.timestamp
        } for post in posts]

    return jsonify(all_posts), 200


@social.route("/api/social/comment", methods=['POST'])
@jwt_required
def comment():
    data = request.json

    if Posts.query.filter_by(post_id=data['post_id']).first() is None:
        return jsonify({"msg": "Post does not exist."}), 500

    comment_user_id = Users.query.filter_by(username=data['username']).first()

    comment = Comments(user_id=comment_user_id.user_id, post_id=data['post_id'], text=data['text'])
    db.session.add(comment)
    db.session.commit()
    return jsonify({"msg": "Comment created."}), 201


@social.route("/api/social/comment", methods=['GET'])
@jwt_required
def get_comments():
    data = request.json

    if Posts.query.filter_by(post_id=data['post_id']).first() is None:
        return jsonify({"msg": "Post does not exist."}), 500

    comments = Comments.query.filter_by(post_id=data['post_id']).all()

    all_comments = [{
        'comment_id': comment.comment_id,
        'user_id': comment.user_id,
        'post_id': comment.post_id,
        'text': comment.text
        } for comment in comments]

    return jsonify(all_comments), 200


@social.route("/api/social/like", methods=['POST'])
@jwt_required
def like():
    data = request.json

    if Users.query.filter_by(username=data['username']).first() is None:
        return jsonify({"msg": "User does not exist."}), 500
    elif Posts.query.filter_by(post_id=data['post_id']).first() is None:
        return jsonify({"msg": "Post does not exist."}), 500
    elif Comments.query.filter_by(comment_id=data['comment_id']).first() is None and data['comment_id'] is not None:
        return jsonify({"msg": "Comment does not exist."}), 500

    like_user_id = Users.query.filter_by(username=data['username']).first()

    like = Likes(user_id=like_user_id.user_id, post_id=data['post_id'], comment_id=data['comment_id'])
    db.session.add(like)
    db.session.commit()
    return jsonify({"msg": "Like created."}), 201


@social.route("/api/social/like", methods=['GET'])
@jwt_required
def get_likes():
    data = request.json

    if Posts.query.filter_by(post_id=data['post_id']).first() is None:
        return jsonify({"msg": "Post does not exist."}), 500
    elif Comments.query.filter_by(comment_id=data['comment_id']).first() is None and data['comment_id'] is not None:
        return jsonify({"msg": "Comment does not exist."}), 500

    likes = Likes.query.filter_by(post_id=data['post_id'], comment_id=data['comment_id']).all()

    all_likes = [{
        'like_id': like.like_id,
        'user_id': like.user_id,
        'post_id': like.post_id,
        'comment_id': like.comment_id
        } for like in likes]

    return jsonify(all_likes), 200


@social.route("/api/social/directmessage", methods=['POST'])
@jwt_required
def direct_message():
    data = request.json

    sender_user_id = Users.query.filter_by(username=data['sender_username']).first()
    receiver_user_id = Users.query.filter_by(username=data['receiver_username']).first()

    direct_message = Direct_Messages(sender_id=sender_user_id.user_id, receiver_id=receiver_user_id.user_id, text=data['text'], spotify_data=data['spotify_data'])
    db.session.add(direct_message)
    db.session.commit()
    return jsonify({"msg": "Direct Message sent."}), 201


@social.route("/api/social/directmessage/<user_name>", methods=['GET'])
@jwt_required
def get_direct_message(user_name):
    if Users.query.filter_by(username=user_name).first() is None:
        return jsonify({"msg": "Sending user does not exist."}), 500

    dm_user_id = Users.query.filter_by(username=user_name).first()

    sent_direct_messages = Direct_Messages.query.filter_by(sender_id=dm_user_id.user_id)
    received_direct_messages = Direct_Messages.query.filter_by(receiver_id=dm_user_id.user_id)

    sent_dms = [{
        'message_id': dm.message_id,
        'sender_id': dm.sender_id,
        'receiver_id': dm.receiver_id,
        'text': dm.text,
        'spotify_data': dm.spotify_data,
        'timestamp': dm.timestamp
        } for dm in sent_direct_messages]

    received_dms = [{
        'message_id': dm.message_id,
        'sender_id': dm.sender_id,
        'receiver_id': dm.receiver_id,
        'text': dm.text,
        'spotify_data': dm.spotify_data,
        'timestamp': dm.timestamp
        } for dm in received_direct_messages]

    return jsonify(sent_dms + received_dms), 200


@social.route("/api/social/followrequest", methods=['POST'])
@jwt_required
def follow_request():
    data = request.json

    sender_user_id = Users.query.filter_by(username=data['sender_username']).first()
    receiver_user_id = Users.query.filter_by(username=data['receiver_username']).first()

    follow_request = Follow_Requests(sender_id=sender_user_id.user_id, receiver_id=receiver_user_id.user_id)
    db.session.add(follow_request)
    db.session.commit()
    return jsonify({"msg": "Follow Request sent."}), 201


@social.route("/api/social/followrequest/<user_name>", methods=['GET'])
@jwt_required
def get_requests(user_name):
    if Users.query.filter_by(username=user_name).first() is None:
        return jsonify({"msg": "User does not exist."}), 500

    request_user_id = Users.query.filter_by(username=user_name).first()

    follow_requests = Follow_Requests.query.filter_by(receiver_id=request_user_id.user_id).all()

    all_requests = [{
        'request_id': request.request_id,
        'sender_id': request.sender_id,
        'receiver_id': request.receiver_id,
        'timestamp': request.timestamp
        } for request in follow_requests]

    return jsonify(all_requests), 200


@social.route("/api/social/relationship", methods=['POST'])
@jwt_required
def relationship():
    data = request.json

    if Users.query.filter_by(username=data['follower_username']).first() is None:
        return jsonify({"msg": "Follower user does not exist."}), 500
    elif Users.query.filter_by(username=data['followed_username']).first() is None:
        return jsonify({"msg": "Followed user does not exist."}), 500

    follower_relationship_id = Users.query.filter_by(username=data['follower_username']).first()
    followed_relationship_id = Users.query.filter_by(username=data['followed_username']).first()

    relationship = Follow_Relationship(follower_id=follower_relationship_id.user_id, followed_id=followed_relationship_id.user_id)
    db.session.add(relationship)
    db.session.commit()
    return jsonify({"msg": "Relationship created."}), 201



@social.route("/api/social/relationship/<user_name>", methods=['GET'])
@jwt_required
def get_relationships(user_name):
    if Users.query.filter_by(username=user_name).first() is None:
        return jsonify({"msg": "User does not exist."}), 500

    relationship_user_id = Users.query.filter_by(username=user_name).first()

    follower_relationships = Follow_Relationship.query.filter_by(follower_id=relationship_user_id.user_id)
    followed_relationships = Follow_Relationship.query.filter_by(followed_id=relationship_user_id.user_id)

    all_follower_relationships = [{
        'relationship_id': relationship.relationship_id,
        'follower_id': relationship.follower_id,
        'follower_id': relationship.followed_id,
        'timestamp': relationship.timestamp
        } for relationship in follower_relationships]

    all_followed_relationships = [{
        'relationship_id': relationship.relationship_id,
        'follower_id': relationship.follower_id,
        'follower_id': relationship.followed_id,
        'timestamp': relationship.timestamp
        } for relationship in followed_relationships]

    return jsonify(all_follower_relationships + all_followed_relationships), 200
