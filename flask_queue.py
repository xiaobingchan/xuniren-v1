from flask import Flask, jsonify
import queue
import threading
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import time
from flask import request

#星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/ofka93cgeoap_v1'
#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = '77688bc2'
SPARKAI_API_SECRET = 'MDJhY2ZjYzdjYWVmYjgxN2JjMjY4MWJk'
SPARKAI_API_KEY = '5f0c90d03723a56535962a5b7733664f'
#星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'generalv3.5'
spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=True,
    )

app = Flask(__name__)

# 创建一个队列
data_queue = queue.Queue()

# 处理函数
def process_queue():
    while True:
        # 从队列中获取数据
        data = data_queue.get()
        if data is None:  # 用于结束线程
            break
            
        # 处理数据
        print(f"Processing: {data}")
        data_queue.task_done()

# 启动后台线程
thread = threading.Thread(target=process_queue, daemon=True)
thread.start()

@app.route('/xfzhinengti_chat_steaming', methods=['POST'])
def add_to_queue():
    data = request.form
    data_message = data.get("message")
    messages = [ChatMessage(
        role="user",
        content=data_message
    )]
    # handler = ChunkPrintHandler()
    # result = spark.generate([messages], callbacks=[handler])
    # text_content = result.generations[0][0].text
    a = spark.stream(messages)
    for message in a:
        print(message)
        data_queue.put(message)
    return jsonify({"message": "Data added to queue", "data": data}), 201

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({"queue_size": data_queue.qsize()}), 200

if __name__ == '__main__':
    app.run(debug=True)