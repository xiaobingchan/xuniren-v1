from flask import Flask, jsonify
import queue
import threading
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import time
from flask import request
import json
from flask import Response

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

@app.route('/xfzhinengti_chat_steaming', methods=['POST'])
def add_to_queue():
    data = request.form
    data_message = data.get("message")
    messages = [ChatMessage(
        role="user",
        content=data_message
    )]
    a = spark.stream(messages)
    # for message in a:
    #     print(message)
    #     data_queue.put(message)
    def generate():
        for message in a:
            message=str(message).replace('\'', '').replace('content=', '').replace('data: ', '')
            if 'additional_kwargs' not in message and len(message) > 1:
                yield f"{message}\n\n".encode('utf-8')  # 将字符串转换为字节数据并添加换行符
    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }
    return Response(generate(), mimetype="text/event-stream", headers=headers)

if __name__ == '__main__':
    app.run(debug=True)


# $uri = 'http://127.0.0.1:5000/xfzhinengti_chat_steaming'
# $message = '你是谁'
# $body = @{ message = $message }
# Invoke-RestMethod -Uri $uri -Method Post -ContentType 'application/x-www-form-urlencoded' -Body $body