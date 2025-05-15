from datetime import datetime
from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    runs = db.relationship('Run', backref='player', cascade='all, delete-orphan')
    discussions = db.relationship('Discussion', backref='author', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', cascade='all, delete-orphan')

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bio = db.Column(db.Text)
    telegram = db.Column(db.String(50))
    discord = db.Column(db.String(50))
    avatar_url = db.Column(db.String(255))

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.Integer, nullable=False)
    league = db.Column(db.String(20), nullable=False)
    runs = db.relationship('Run', backref='challenge', cascade='all, delete-orphan')

class Run(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    video_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='run', cascade='all, delete-orphan')

class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='discussion', cascade='all, delete-orphan')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    discussion_id = db.Column(db.Integer, db.ForeignKey('discussion.id'))
    run_id = db.Column(db.Integer, db.ForeignKey('run.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), cascade='all, delete-orphan')