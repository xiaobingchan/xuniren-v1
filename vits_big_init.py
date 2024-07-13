speakername="Yennefer"
import requests
import json
url = "http://127.0.0.1:5000/models/get_local?root_dir=Data"
payload={}
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}
response = requests.request("GET", url, headers=headers, data=payload)
pathlist=json.loads(response.text)
print(pathlist)

# {'lyl': ['G_jzo1.pth'], 'Yennefer': ['models/G_0.pth', 'models/G_50.pth', 'models/G_100.pth', 'models/G_150.pth']}

last_file = pathlist[speakername][-1] # models/G_150.pth
print(last_file)

import requests
url = "http://127.0.0.1:5000/models/add?model_path=Data/"+speakername+"/"+last_file+"&device=cuda:0&language=ZH"
payload={}
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}
response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)

# {"status":0,"detail":"模型添加成功","Data":{"model_id":0,"model_info":{"config_path":"Data\\Yennefer\\config.json","model_path":"D:\\Bert-VITS2-Extra\\Data\\Yennefer\\models\\G_150.pth","device":"cuda:0","language":"ZH","spk2id":{"Yennefer":0},"id2spk":{"0":"Yennefer"},"version":"2.3"}}}

output="你好吗"
import requests
url = "http://127.0.0.1:5000/voice?model_id=0&speaker_name="+speakername+"&sdp_ratio=0.2&noise=0.2&noisew=0.9&length=1&language=ZH&auto_translate=false&auto_split=false&emotion=&style_weight=0.7"
payload={"text":output}
files=[
]
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}
response = requests.request("POST", url, headers=headers, data=payload, files=files)
# 将文件流写入到 WAV 文件
with open("output.wav", "wb") as f:
    f.write(response.content)
print("File saved as output.wav")
