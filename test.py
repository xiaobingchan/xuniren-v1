# import alitts
# wav_file="test.wav"
# output="你好"
# alitts.speakword(wav_file,output)

import requests
import time

url = 'https://ark.cn-beijing.volces.com/api/v3/bots/chat/completions'
headers = {
    'Authorization': 'Bearer df597f4e-3f9d-4cfe-968f-0bade2f7b79a',
    'Content-Type': 'application/json'
}
data = {
    "model": "bot-20240921105732-frfdn",
    "stream": False,
    "stream_options": {"include_usage": True},
    "messages": [
        {
            "role": "user",
            "content": "介绍下公司"
        }
    ]
}
# 计算程序运行时间
start_time = time.time()
response = requests.post(url, headers=headers, json=data)
response_data = response.json()
content = response_data['choices'][0]['message']['content']
print(content)
# 计算程序运行时间
end_time = time.time()
print(f"程序运行时间：{end_time - start_time}秒")