from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config

# Инициализация приложения
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Импорт моделей после инициализации db
from models import User, UserProfile, Challenge, Run, Discussion, Comment

# Вспомогательные функции
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Декораторы для проверки прав
def moderator_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        if not user or user.role != 'moderator':
            return jsonify({"msg": "Moderator access required"}), 403
        return fn(*args, **kwargs)
    return wrapper

# API endpoints
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already exists"}), 400
    
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        password_hash=hashed_password,
        email=data['email']
    )
    db.session.add(new_user)
    db.session.commit()
    
    # Create empty profile
    profile = UserProfile(user_id=new_user.id)
    db.session.add(profile)
    db.session.commit()
    
    return jsonify({"msg": "User created successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({"msg": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token), 200

@app.route('/api/profile/<username>')
def get_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify({
        "username": user.username,
        "bio": user.profile.bio if user.profile else None,
        "telegram": user.profile.telegram if user.profile else None,
        "discord": user.profile.discord if user.profile else None,
        "avatar": user.profile.avatar_url if user.profile else None,
        "runs": [{
            "id": run.id,
            "challenge": run.challenge.name,
            "status": run.status,
            "submitted_at": run.submitted_at.isoformat()
        } for run in user.runs],
        "discussions": [{
            "id": disc.id,
            "title": disc.title,
            "created_at": disc.created_at.isoformat()
        } for disc in user.discussions]
    })

@app.route('/api/leaderboard')
def get_leaderboard():
    users = User.query.all()
    ranked_users = []
    
    for user in users:
        approved_runs = [run for run in user.runs if run.status == 'approved']
        if approved_runs:
            max_difficulty = max(run.challenge.difficulty for run in approved_runs)
            league = approved_runs[0].challenge.league
            ranked_users.append({
                "username": user.username,
                "max_difficulty": max_difficulty,
                "league": league,
                "runs_count": len(approved_runs)
            })
    
    ranked_users.sort(key=lambda x: (-x['max_difficulty'], -x['runs_count']))
    return jsonify(ranked_users)

@app.route('/api/runs', methods=['POST'])
@jwt_required()
def submit_run():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    data = request.get_json()
    challenge = Challenge.query.get(data['challenge_id'])
    if not challenge:
        return jsonify({"msg": "Challenge not found"}), 404
    
    new_run = Run(
        user_id=user.id,
        challenge_id=challenge.id,
        video_url=data['video_url'],
        description=data.get('description', '')
    )
    db.session.add(new_run)
    db.session.commit()
    
    return jsonify({"msg": "Run submitted for moderation", "run_id": new_run.id}), 201

@app.route('/api/runs/<int:run_id>/approve', methods=['POST'])
@moderator_required
def approve_run(run_id):
    run = Run.query.get_or_404(run_id)
    run.status = 'approved'
    run.approved_at = datetime.utcnow()
    db.session.commit()
    
    socketio.emit('run_approved', {
        'user_id': run.user_id,
        'run_id': run.id,
        'challenge': run.challenge.name
    }, room=f'user_{run.user_id}')
    
    return jsonify({"msg": "Run approved"})

@app.route('/api/discussions', methods=['POST'])
@jwt_required()
def create_discussion():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    data = request.get_json()
    new_discussion = Discussion(
        title=data['title'],
        content=data['content'],
        author_id=user.id
    )
    db.session.add(new_discussion)
    db.session.commit()
    
    return jsonify({"msg": "Discussion created", "discussion_id": new_discussion.id}), 201

@app.route('/api/discussions/<int:discussion_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(discussion_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    data = request.get_json()
    new_comment = Comment(
        content=data['content'],
        author_id=user.id,
        discussion_id=discussion_id,
        parent_id=data.get('parent_id')
    )
    db.session.add(new_comment)
    db.session.commit()
    
    discussion = Discussion.query.get(discussion_id)
    socketio.emit('new_comment', {
        'discussion_id': discussion_id,
        'comment_id': new_comment.id,
        'author': user.username,
        'content': new_comment.content
    }, room=f'discussion_{discussion_id}')
    
    return jsonify({"msg": "Comment added", "comment_id": new_comment.id}), 201

# WebSocket handlers
@socketio.on('connect')
def handle_connect():
    user = get_jwt_identity()
    if user:
        join_room(f'user_{user.id}')
        emit('connection_status', {'status': 'connected'})

@socketio.on('join_discussion')
def handle_join_discussion(data):
    discussion_id = data['discussion_id']
    join_room(f'discussion_{discussion_id}')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')