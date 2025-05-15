from app import create_app
from app.extensions import socketio, db
from app.models import User, UserProfile, Challenge, Run, Discussion, Comment

app = create_app()

@app.cli.command('initdb')
def initdb_command():
    """Initialize the database."""
    db.create_all()
    print('Initialized the database.')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)