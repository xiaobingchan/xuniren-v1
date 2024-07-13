# server.py
from flask import Flask, request, jsonify
from flask_sockets import Sockets
import base64
import time
import json
import gevent
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import os
import re
import numpy as np
import shutil
import asyncio
app = Flask(__name__)
sockets = Sockets(app)
video_list = []
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

async def main(voicename: str, text: str, OUTPUT_FILE):
    print('main开始！')

def send_information(path, ws):
    print('传输信息开始！')
    with open(path, 'rb') as f:
        video_data = base64.b64encode(f.read()).decode()
    data = {
            'video': 'data:video/mp4;base64,%s' % video_data,
            }
    json_data = json.dumps(data)
    ws.send(json_data)

@sockets.route('/dighuman')
def echo_socket(ws):
    # 获取WebSocket对象
    #ws = request.environ.get('wsgi.websocket')
    # 如果没有获取到，返回错误信息
    if not ws:
        print('未建立连接！')
        return 'Please use WebSocket'
    # 否则，循环接收和发送消息
    else:
        print('建立连接！')
        while True:
            message = ws.receive()
            if len(message)==0:
                return '输入信息为空'
            else:                                                    
                output_path = message
                send_information(output_path, ws)
                

if __name__ == '__main__':

    server = pywsgi.WSGIServer(('0.0.0.0', 8802), app, handler_class=WebSocketHandler)
    server.serve_forever()
    
    