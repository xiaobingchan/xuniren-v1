from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    print(f"Received message: {data}")
    # 处理特定数据，例如只对“hello”做出响应
    if data == "hello":
        response = "Hello, client!"
    else:
        response = "Unknown message"
    emit('response', response)

if __name__ == '__main__':
    socketio.run(app, debug=True)