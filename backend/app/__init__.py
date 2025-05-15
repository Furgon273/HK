from flask import Flask
from .config import Config
from .extensions import db, jwt, socketio, migrate
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, resources={r"/api/*": {"origins": "*"}})  # Разрешить все домены
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    migrate.init_app(app, db)

    # Register blueprints
    from .routes import bp
    app.register_blueprint(bp)

    return app