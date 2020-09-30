from flask import Flask, render_template, jsonify, request , redirect , url_for, session
from flask_socketio import SocketIO, join_room, leave_room

# ----------------- app configurations -----------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sanfkabjkfbjkdbfj'
socketio = SocketIO(app, manage_session=False)

@app.route('/')
def home():
  return "Hello world"

@app.route('/suggestions')
def suggestions():
  return render_template('suggestion.html')

if __name__ == "__main__":
    socketio.run(app, debug=True)

