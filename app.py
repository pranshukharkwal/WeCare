from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit

# ----------------- app configurations -----------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sanfkabjkfbjkdbfj'
socketio = SocketIO(app, manage_session=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/yoga', methods=['GET'])
def yoga_page():
    return render_template('yoga.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['room'] = request.form['room']
        return redirect(url_for('.chatroom'))
    else:
        return render_template('chat.html')


@app.route('/chatroom')
def chatroom():
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.chat'))
    return render_template('chatroom.html', name=name, room=room)


@app.route('/suggestions')
def suggestions():
    return render_template('suggestion.html')


@app.route('/time', methods=['POST', 'GET'])
def time():
    if request.method == 'POST':
        userKey = request.form['userKey']
        displayName = request.form['displayName']
        print("User key", userKey, displayName)
        session['userKey'] = userKey
        session['displayName'] = displayName
        return jsonify(success=1, userKey=userKey, displayName=displayName)
        # So after the post, reload the page

    else:
        # Now for both of them
        userKey = ''
        displayName = ''
        if 'userKey' in session:
            print("User exist", session['userKey'])
            userKey = session['userKey']
            displayName = session['displayName']
        return render_template('time.html', userKey=userKey, displayName=displayName)


@app.route('/time/logout', methods=['POST', 'GET'])
def time_logout():
    session.pop('userKey')
    try:
        print('removing userkey', session['userKey'])
    except:
        print("Removing userKey done")
    return redirect(url_for('time'))


@app.route('/medication')
def medication():
    return render_template('medication.html')

# @app.route('/shortgoals')
# def sg():
#     return render_template('shortgoals.html')

# @app.route('/longgoals')
# def lg():
#     return render_template('longgoals.html')


@app.route('/timetable')
def tt():
    return render_template('timetable.html')


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') +
                    ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') +
                     ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') +
                    ' has left the room.'}, room=room)


if __name__ == "__main__":
    socketio.run(app, debug=True)
