from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
SocketIO = SocketIO(app)

users = {}

@app.route('/')
def index():
    return render_template('index.html')

#We're listtening to the connect event from the client.

@SocketIO.on('connect')
def handle_connect():
    print('Client connected')
    userName = f"User{random.randint(1, 1000)}"
    iconStyle = random.choice(['girl', 'boy'])
    iconURL = f"https://avatar.iran.liara.run/public/{iconStyle}?username={userName}"
    users[request.sid] = {'userName': userName,'iconURL': iconURL}

    emit('user_connected', {'userName': userName, 'iconURL': iconURL})
    emit("new_user_connected", {'userName': userName}, broadcast=True)

@SocketIO.on('change_username')
def handle_change_username(data):
    print('Username change requested:', data)
    newUserName = data['newUserName']

    if request.sid in users:
        oldUserName = users[request.sid]['userName']
        users[request.sid]['userName'] = newUserName

        emit('username_changed', {'oldUserName': oldUserName, 'newUserName': newUserName}, broadcast=True)
        emit("username", newUserName)

@SocketIO.on('disconnect')
def handle_disconnect():
    print('Client disconnecting')
    currentUser = users[request.sid]['userName']

    emit('user_disconnected', {'userName': currentUser}, broadcast=True)
    emit("disconnected", currentUser)

    users.pop(request.sid, None)

@SocketIO.on('send_message')
def handle_send_message(data):
    print('Message received:', data)
    userName = users[request.sid]['userName']
    iconURL = users[request.sid]['iconURL']

    message = {
        'userName': userName,
        'iconURL': iconURL,
        'message': data['message']
    }

    emit('receive_message', message, broadcast=True)

if __name__ == '__main__':
    SocketIO.run(app)