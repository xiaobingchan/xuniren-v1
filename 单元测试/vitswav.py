import requests

wav_file='test.wav'
output='你吃饭了吗'
url = 'http://readvoice.qnxr.ltd:8080'
params = {
    'speaker': 'jz01',
    'text': output,
    'language': 'ZH'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    with open(wav_file, 'wb') as f:
        f.write(response.content)
        print('文件已保存为 test.wav')
else:
    print('请求失败:', response.status_code)

