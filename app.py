from crypt import methods
from distutils.log import debug
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from flask_socketio import SocketIO, send, emit, leave_room, join_room

app = Flask(__name__)
app.debug = True
app.config['SECRET'] = "secret!123"
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False)


@socketio.on('message')
def message(message):
    print("Received message: " + message)
    username = session.get('username')
    room = session.get('room')
    join_room(room)
    if message == "User joined!":
        send(username+" has entered the room.", broadcast=True, room=room)
    else:
        send(username+": " + message, broadcast=True, room=room)


@socketio.on('disconnect')
def disconnect():
    username = session.get('username')
    room = session.get('room')
    leave_room(room)
    send(username+" has left the room.", broadcast=True, room=room)
    session.clear()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        room = request.form['room']
        # Store the data in session
        session['username'] = username
        session['room'] = room
        return redirect('/chat')
    else:
        return render_template('index.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        pass
    else:
        return render_template('chat.html', session=session)


if __name__ == "__main__":
    socketio.run(app, host="localhost", port=4999)
