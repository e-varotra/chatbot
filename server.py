from flask import Flask , render_template , request, redirect, url_for
from flask_socketio import SocketIO, join_room

import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app)



@app.route('/')
def home():
    return render_template("index.html")

@app.route('/socket.io.js')
def socketio_js():
    print('lien')
    return app.send_static_file('socket.io.js')

@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('chat.html' ,  username=username, room=room)
    else:
        return redirect(url_for('home'))

@socketio.on('envoie_message')
def handle_send_message_event(data):
    app.logger.info("{} a envoyer un message au room {}".format(data['username'],data['room'],data['message']))

    socketio.emit('recu_msg', data, room=data['room'])

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} a rejoin le room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('annoncement_join_room', data)

#socketio = SocketIO(app, async_mode='eventlet')

if __name__ == "__main__" :
    socketio.run(app, debug=True)



