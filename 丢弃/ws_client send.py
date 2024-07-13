import threading
import asyncio
import websockets

def send_message(message):
    async def send():
        async with websockets.connect('ws://localhost:60001') as ws:
            await ws.send(message)
            print("消息已发送")
            await ws.close()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send())

# 创建一个线程来执行发送消息操作
def send_message_thread(message):
    send_message(message)

# 获取用户输入的消息
message = "你好"

# 创建一个后台多线程，并传递用户输入的消息作为参数
thread = threading.Thread(target=send_message_thread, args=(message,))
thread.daemon = True  # 设置线程为后台线程，当主线程退出时，后台线程也会退出
thread.start()

# 主线程继续执行其他操作
print("主线程继续执行其他操作")

# 让主线程等待后台线程执行完毕
thread.join()