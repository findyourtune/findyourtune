from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from backend import db, ma


class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    bio = db.Column(db.Text, nullable=True)
    spotify_account = db.Column(db.String(120), nullable=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.user_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# TODO: Implement Schema for each of our tables
# Marshmallow is used for serialization/deserialization of Python data types for API calls
class UsersSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Users

    user_id = ma.auto_field()
    username = ma.auto_field()
    firstname = ma.auto_field()
    lastname = ma.auto_field()
    password = ma.auto_field()
    email = ma.auto_field()
    image_file = ma.auto_field()
    bio = ma.auto_field()
    spotify_account = ma.auto_field()


class Posts(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    spotify_data = db.Column(db.String(240), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Post(post_id: '{self.post_id}', user_id: '{self.user_id}', timestamp: '{self.timestamp}')"


class PostsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Posts

    post_id = ma.auto_field()
    user_id = ma.auto_field()
    text = ma.auto_field()
    spotify_data = ma.auto_field()
    timestamp = ma.auto_field()


class Comments(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Comment(comment_id: '{self.comment_id}', user_id: '{self.user_id}')"


class CommentsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Comments

    comment_id = ma.auto_field
    user_id = ma.auto_field
    text = ma.auto_field


class Likes(db.Model):
    __tablename__ = 'likes'
    like_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'), nullable=True)

    def __repr__(self):
        return f"Like(like_id: '{self.like_id}', user_id: '{self.user_id}')"


class LikesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Likes

    like_id = ma.auto_field
    user_id = ma.auto_field
    post_id = ma.auto_field
    comment_id = ma.auto_field


class Direct_Messages(db.Model):
    __tablename__ = 'directmessages'
    message_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    spotify_data = db.Column(db.String(240), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"DirectMessages(message_id: '{self.message_id}', timestamp: '{self.timestamp}')"


class DirectMessagesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Direct_Messages
    
    message_id = ma.auto_field
    sender_id = ma.auto_field
    receiver_id = ma.auto_field
    text = ma.auto_field
    spotify_data = ma.auto_field
    timestamp = ma.auto_field


class Follow_Requests(db.Model):
    __tablename__ = 'requests'
    request_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Request(request_id: '{self.request_id}', timestamp: '{self.timestamp}')"


class FollowRequestsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Follow_Requests
    
    request_id = ma.auto_field
    sender_id = ma.auto_field
    receiver_id = ma.auto_field
    timestamp = ma.auto_field


class Follow_Relationship(db.Model):
    __tablename__ = 'relationships'
    relationship_id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Relationship(relationship_id: '{self.request_id}', timestamp: '{self.timestamp}')"


class FollowRelationshipSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Follow_Relationship
    
    relationship_id = ma.auto_field
    follower_id = ma.auto_field
    followed_id = ma.auto_field
    timestamp = ma.auto_field