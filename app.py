from flask import Flask, render_template, jsonify, request , redirect , url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit

# ----------------- app configurations -----------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sanfkabjkfbjkdbfj'
socketio = SocketIO(app, manage_session=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['room'] = request.form['room']
        return redirect(url_for('.chat'))
    else:
        return render_template('index.html')


@app.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)

@app.route('/suggestions')
def suggestions():
  return render_template('suggestion.html')

@app.route('/medication')
def medication():
    return render_template('medication.html')


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)



if __name__ == "__main__":
    socketio.run(app, debug=True)

