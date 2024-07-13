import requests
import os

usd_file_name = "DefaultOfficialInstance.usd"
usd_absolute_path = os.path.abspath(usd_file_name)
print(usd_absolute_path)

url = 'http://127.0.0.1:10246/A2F/USD/Load'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
data = {
    'file_name': usd_absolute_path
}

response = requests.post(url, headers=headers, json=data)

wav_name = "test.wav"
wav_absolute_pathdir = os.path.abspath(wav_name).replace("\\test.wav","")
print(wav_absolute_pathdir)
url = 'http://127.0.0.1:10246/A2F/Player/SetRootPath'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
data = {
    'a2f_player': '/World/audio2face/Player',
    'dir_path': wav_absolute_pathdir
}

response = requests.post(url, headers=headers, json=data)

print("初始化完成")

import requests

url = 'http://127.0.0.1:10246/A2F/Player/SetTrack'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
data = {
    'a2f_player': '/World/audio2face/Player',
    'file_name': 'test.wav',
    'time_range': [0, -1]
}

response = requests.post(url, headers=headers, json=data)

import requests

url = 'http://127.0.0.1:10246/A2F/Player/Play'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
data = {
    'a2f_player': '/World/audio2face/Player'
}

response = requests.post(url, headers=headers, json=data)