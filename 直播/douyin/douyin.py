# -*- coding: utf-8 -*-
import asyncio
import random
from tkinter import *
import subprocess
from collections import deque
import asyncio
import websockets
import json
import requests
import socket
import websockets as ws
import threading

def send_message(msg):
    async def send():
        async with websockets.connect('ws://localhost:60001') as ws:
            await ws.send(msg)
            print("消息已发送")
            await ws.close()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send())

# 创建一个线程来执行发送消息操作
def send_message_thread(msg):
    send_message(msg)


async def get_data():
    async with websockets.connect('ws://127.0.0.1:8888',ping_interval =None) as websocket:
        while True:
        # 接收消息
            message = await websocket.recv()
            message =  json.loads(message,strict=False)
            if(message['Type']==1):
                msg =  json.loads(message['Data'],strict=False)
                print(msg['Content'])
                result=msg['Content']
                # 创建一个后台多线程，并传递用户输入的消息作为参数
                thread = threading.Thread(target=send_message_thread, args=(result,))
                thread.daemon = True  # 设置线程为后台线程，当主线程退出时，后台线程也会退出
                thread.start()
            if(message['Type']==3):
                msg =  json.loads(message['Data'],strict=False)
                nickname = msg['User']['Nickname']
                result = "欢迎"+nickname+"来到直播间"
                print(result)
                # 创建一个后台多线程，并传递用户输入的消息作为参数
                thread = threading.Thread(target=send_message_thread, args=(result,))
                thread.daemon = True  # 设置线程为后台线程，当主线程退出时，后台线程也会退出
                thread.start()
            if(message['Type']==5):
                msg =  json.loads(message['Data'],strict=False)
                nickname = msg['User']['Nickname']
                result = "感谢"+nickname+"送到礼物"
                print(result)
                # 创建一个后台多线程，并传递用户输入的消息作为参数
                thread = threading.Thread(target=send_message_thread, args=(result,))
                thread.daemon = True  # 设置线程为后台线程，当主线程退出时，后台线程也会退出
                thread.start()
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(get_data())


	
