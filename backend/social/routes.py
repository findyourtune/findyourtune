import os
from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, session, current_app
from flask_session import Session
from flask_wtf import Form
from flask_jwt_extended import jwt_required
from wtforms.fields.html5 import DateField
import uuid
import jwt
from backend import db
from sqlalchemy.orm import aliased


from backend.models import Users, Posts, Comments, Likes, Direct_Messages, Follow_Requests, Follow_Relationship, Users, UsersSchema
from backend.auth.utils import get_user_info_from_token

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

    if Users.query.filter_by(user_id=data['user_id']).first() is None:
        return jsonify({"msg": "User does not exist."}), 500

    post = Posts(user_id=data['user_id'], text=data['text'], spotify_data=data['spotify_data'])
    db.session.add(post)
    db.session.commit()
    return jsonify({"msg": "Post created."}), 201


@social.route("/api/social/delete_post", methods=['POST'])
@jwt_required
def delete_post():
    data = request.json
    current_user = get_user_info_from_token(request)

    if current_user is not None:
        current_user_id = current_user['user_id']
    else:
        current_user_id = None

    if Users.query.filter_by(user_id=data['user_id']).first() is None:
        return jsonify({"msg": "User does not exist."}), 500

    if Posts.query.filter_by(post_id=data['post_id']).first() is None:
        return jsonify({"msg": "Post does not exist."}), 500

    if current_user_id != data['user_id']:
        return jsonify({"msg": "Can only delete owned posts."}), 500

    Posts.query.filter_by(post_id=data['post_id']).delete()
    db.session.commit()
    return jsonify({"msg": "Post deleted."}), 201


@social.route("/api/social/get_posts", methods=['GET'])
def get_posts():
    current_user = get_user_info_from_token(request)

    if current_user is not None:
        current_user_id = current_user['user_id']
    else:
        current_user_id = None

    posts = db.session.query(Posts, Users.username.label('username'), Users.firstname.label('firstname'), Users.lastname.label('lastname'), Users.appcolor.label('appColor'))\
                        .join(Users, Users.user_id == Posts.user_id)\
                        .order_by(Posts.timestamp.desc()).all()

    all_posts = [{
        'post_id': post.Posts.post_id, 
        'user_id': post.Posts.user_id, 
        'name': post.firstname + " " + post.lastname,
        'firstname': post.firstname,
        'lastname': post.lastname,
        'username': post.username,
        'text': post.Posts.text, 
        'appColor': post.appColor,
        'spotify_data': post.Posts.spotify_data, 
        'timestamp': post.Posts.timestamp,
        'current_user_likes': db.session.query(Likes).filter_by(user_id=current_user_id, post_id=post.Posts.post_id).first() is not None
        } for post in posts]

    return jsonify(all_posts), 200

@social.route("/api/social/get_posts/<username>", methods=['GET'])
def get_posts_user(username):
    current_user = get_user_info_from_token(request)

    if current_user is not None:
        current_user_id = current_user['user_id']
    else:
        current_user_id = None
    
    posts = db.session.query(Posts, Users.username.label('username'), Users.firstname.label('firstname'), Users.lastname.label('lastname'), Users.appcolor.label('appColor'))\
                        .join(Users, Users.user_id == Posts.user_id)\
                        .filter(Users.username == username)\
                        .order_by(Posts.timestamp.desc()).all()

    all_posts = [{
        'post_id': post.Posts.post_id, 
        'user_id': post.Posts.user_id, 
        'name': post.firstname + " " + post.lastname,
        'firstname': post.firstname,
        'lastname': post.lastname,
        'username': post.username,
        'text': post.Posts.text, 
        'appColor': post.appColor,
        'spotify_data': post.Posts.spotify_data, 
        'timestamp': post.Posts.timestamp,
        'current_user_likes': db.session.query(Likes).filter_by(user_id=current_user_id, post_id=post.Posts.post_id).first() is not None
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


@social.route("/api/social/toggle_like_post", methods=['POST'])
@jwt_required
def toggle_like_post():
    data = request.json
    current_user = get_user_info_from_token(request)

    if current_user is not None:
        current_user_id = current_user['user_id']
    else:
        current_user_id = None

    if current_user_id == data['post_user_id']:
        return jsonify({"msg": "Cannot like own post."}), 500

    if Users.query.filter_by(user_id=data['user_id']).first() is None:
        return jsonify({"msg": "User does not exist."}), 500

    if Posts.query.filter_by(post_id=data['post_id']).first() is None:
        return jsonify({"msg": "Post does not exist."}), 500

    liked = Likes.query.filter_by(user_id=data['user_id'], post_id=data['post_id']).first()
    if liked is None:
        like = Likes(user_id=data['user_id'], post_id=data['post_id'])
        db.session.add(like)
        liked = True
    else:
        Likes.query.filter_by(user_id=data['user_id'], post_id=data['post_id']).delete()
        liked = False
    
    db.session.commit()
    return jsonify({"msg": "Post like toggled.", "like": liked}), 201


@social.route("/api/social/get_liked_posts/<username>", methods=['GET'])
def get_liked_posts(username):
    current_user = get_user_info_from_token(request)

    if current_user is not None:
        current_user_id = current_user['user_id']
    else:
        current_user_id = None

    user1 = aliased(Users)
    user2 = aliased(Users) 

    profile_user = Users.query.filter_by(username=username).first()

    posts = db.session.query(Posts, user2.username.label('username'), user2.firstname.label('firstname'), user2.lastname.label('lastname'), user2.appcolor.label('appColor'))\
                        .join(Likes, Likes.post_id == Posts.post_id)\
                        .join(user2, user2.user_id == Posts.user_id)\
                        .filter(Likes.user_id == profile_user.user_id)\
                        .order_by(Likes.timestamp.desc()).all()

    all_posts = [{
        'post_id': post.Posts.post_id, 
        'user_id': post.Posts.user_id, 
        'name': post.firstname + " " + post.lastname,
        'firstname': post.firstname,
        'lastname': post.lastname,
        'username': post.username,
        'text': post.Posts.text, 
        'appColor': post.appColor,
        'spotify_data': post.Posts.spotify_data, 
        'timestamp': post.Posts.timestamp,
        'current_user_likes': db.session.query(Likes).filter_by(user_id=current_user_id, post_id=post.Posts.post_id).first() is not None
        } for post in posts]

    return jsonify(all_posts), 200


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

@social.route("/api/social/follow_user", methods=['POST'])
@jwt_required
def follow_user():
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


@social.route("/api/social/unfollow_user", methods=['POST'])
@jwt_required
def unfollow_user():
    data = request.json

    if Users.query.filter_by(username=data['follower_username']).first() is None:
        return jsonify({"msg": "Follower user does not exist."}), 500
    elif Users.query.filter_by(username=data['followed_username']).first() is None:
        return jsonify({"msg": "Followed user does not exist."}), 500

    follower_relationship_id = Users.query.filter_by(username=data['follower_username']).first()
    followed_relationship_id = Users.query.filter_by(username=data['followed_username']).first()

    Follow_Relationship.query.filter_by(follower_id=follower_relationship_id.user_id, followed_id=followed_relationship_id.user_id).delete()
    db.session.commit()
    return jsonify({"msg": "Relationship created."}), 201


@social.route("/api/social/relationship/<username>", methods=['GET'])
@jwt_required
def get_relationships(username):
    if Users.query.filter_by(username=username).first() is None:
        return jsonify({"msg": "User does not exist."}), 500

    user1 = aliased(Users)
    user2 = aliased(Users)  

    # Follower Relationships                                                
    follower_relationships = db.session.query(user1.username.label('u_username'), user2.username.label('f_username'), user2.firstname.label('f_firstname'), user2.lastname.label('f_lastname'), user2.appcolor.label('f_appColor'), Follow_Relationship)\
                                        .join(Follow_Relationship, (Follow_Relationship.followed_id == user1.user_id))\
                                        .join(user2, user2.user_id == Follow_Relationship.follower_id)\
                                        .filter(user1.username == username)\
                                        .order_by(Follow_Relationship.timestamp.desc()).all()  
    
    # Following Relationships    
    following_relationships = db.session.query(user1.username.label('u_username'), user2.username.label('f_username'), user2.firstname.label('f_firstname'), user2.lastname.label('f_lastname'), user2.appcolor.label('f_appColor'), Follow_Relationship)\
                                        .join(Follow_Relationship, (Follow_Relationship.follower_id == user1.user_id))\
                                        .join(user2, user2.user_id == Follow_Relationship.followed_id)\
                                        .filter(user1.username == username)\
                                        .order_by(Follow_Relationship.timestamp.desc()).all()  
    all_follower_relationships = [{
        'user_username': relationship.f_username,
        'user_firstname': relationship.f_firstname,
        'user_lastname': relationship.f_lastname,
        'user_appcolor': relationship.f_appColor,
        'timestamp': relationship.Follow_Relationship.timestamp
        } for relationship in follower_relationships]

    all_following_relationships = [{
        'user_username': relationship.f_username,
        'user_firstname': relationship.f_firstname,
        'user_lastname': relationship.f_lastname,
        'user_appcolor': relationship.f_appColor,
        'timestamp': relationship.Follow_Relationship.timestamp,
        'user_followed': True
        } for relationship in following_relationships]

    user_follow_rels = {
        'follower_rels': all_follower_relationships,
        'following_rels': all_following_relationships
    }

    return jsonify(user_follow_rels), 200
