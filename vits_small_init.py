speakername="wang"
import requests
import json
url = "http://127.0.0.1:5000/models/get_local?root_dir=Data"
payload={}
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}
response = requests.request("GET", url, headers=headers, data=payload)
pathlist=json.loads(response.text)
last_file = pathlist[speakername][-1] # models/G_150.pth
print(last_file)

{
  "RTE": [
    "models/G_0.pth"
  ],
  "wang": [
    "G_wang.pth"
  ]
}

import requests
url = "http://127.0.0.1:5000/models/add?model_path=Data/wang/G_wang.pth&device=cuda:0&language=ZH"
payload={}
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}
response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)

{"status":0,"detail":"模型添加成功","Data":{"model_id":0,"model_info":{"config_path":"Data\\wang\\config.json","model_path":"D:\\nova_vits\\Bert-VITS2\\Data\\wang\\G_wang.pth","device":"cuda:0","language":"ZH","spk2id":{"wang":0},"id2spk":{"0":"wang"},"version":"2.2"}}}



output="你好吗"
import requests
url = "http://127.0.0.1:5000/voice?model_id=0&speaker_name=wang&sdp_ratio=0.2&noise=0.2&noisew=0.9&length=1&language=ZH&auto_translate=false&auto_split=false&text=你好"
payload={}
files=[]
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}
response = requests.request("POST", url, headers=headers, data=payload, files=files)
print(response.text)
# 将文件流写入到 WAV 文件
with open("output.wav", "wb") as f:
    f.write(response.content)
print("File saved as output.wav")
