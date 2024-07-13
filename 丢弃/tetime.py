from flask import Flask, jsonify
import time

app = Flask(__name__)
last_request_time = 0

@app.route('/apppost', methods=['POST'])
def process_request1():
    global last_request_time
    last_request_time = time.time()
    # 在这里处理第一个接口的请求逻辑
    # ...
    return jsonify({'result': '接口1处理完成'})

@app.route('/daduan', methods=['POST'])
def process_request2():
    global last_request_time
    current_time = time.time()
    elapsed_time = current_time - last_request_time

    if elapsed_time > 10:
        return jsonify({'result': False})
    else:
        return jsonify({'result': True})

if __name__ == '__main__':
    app.run(port=5000, debug=True)