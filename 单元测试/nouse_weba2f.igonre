# pip install click --upgrade

from flask import Flask, request, jsonify
import json
import pyautogui
import time
import os
import pygetwindow as gw
import shutil
import alitts
import contextlib
import librosa
pyautogui.FAILSAFE = False

app = Flask(__name__)
pyautogui.FAILSAFE = False

# 需要修改的地方
relative_x1_rate= 0.974609375 #第二个reset坐标x1比例, 往大调是向右，往小调是向左
relative_y1_rate= 0.154453125 #第二个reset坐标y1比例, 往大调是向下，往小调是向上
relative_x2_rate= 0.929609375 #播放按钮坐标x2比例, 往大调是向右，往小调是向左
relative_y2_rate= 0.234453125 #播放按钮坐标y2比例, 往大调是向下，往小调是向上
wav_file = "F:/audio2face-2023.1.1/audio2face-2023.1.1/exts/omni.audio2face.player_deps/deps/audio2face-data/tracks/test.wav" # 把其他文件都删了，只留下个test.wav

# 获取wav时长
def get_duration(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None) # sr=None 保持原始采样率
        duration = librosa.get_duration(y=y, sr=sr)
        return duration
    except Exception as e:
        print(f"Error with librosa: {e}")
        return None

@app.route('/apppost', methods=['POST'])
def post_example():
    data = request.json
    # 接收 JSON 数据
    # {"message":"你好吗"}
    data_message = data["message"]
    print(data_message)
    
    screen_info = pyautogui.size()
    # second_screen_info = pyautogui.size()  # 第二个屏幕的信息
    width = screen_info.width
    height = screen_info.height
    print("分辨率是：")
    print("Width:", width)
    print("Height:", height)

    # second_screen_info = pyautogui.size()  # 第二个屏幕的信息
    # 移动到屏幕2
    #pyautogui.moveTo(second_screen_info[0], second_screen_info[1])

    # 获取当前打开的所有窗口
    windows = gw.getAllTitles()
    # 打印所有窗口的标题
    for windowname in windows:
        if "release.10" in windowname:
            print("窗口标题:", windowname)
            break
            
    # 获取窗口句柄
    window = gw.getWindowsWithTitle(windowname)[0]  # 替换为你要操作的窗口标题
    # 获取窗口位置
    window_x, window_y = window.left, window.top


    # 根据中文TTS生成wav文件
    output = data_message
    alitts.speakword(wav_file,output)


    # 点击刷新按钮
    relative_x = relative_x1_rate*width  # 例如，要点击窗口内的 x 坐标
    relative_y = relative_y1_rate*height  # 例如，要点击窗口内的 y 坐标

    # 计算绝对坐标
    click_x = window_x + relative_x
    click_y = window_y + relative_y

    # 移动光标到窗口内的相对位置并点击
    pyautogui.moveTo(click_x, click_y, duration=0.1)  # 可选：使用duration控制移动动画
    pyautogui.click()

    # 点击播放按钮
    relative_x = relative_x2_rate*width  # 例如，要点击窗口内的 x 坐标
    relative_y = relative_y2_rate*height  # 例如，要点击窗口内的 y 坐标

    # 计算绝对坐标
    click_x = window_x + relative_x
    click_y = window_y + relative_y

    # 移动光标到窗口内的相对位置并点击
    pyautogui.moveTo(click_x, click_y, duration=0.1)  # 可选：使用duration控制移动动画
    pyautogui.click()
    # 计算音频总长度，秒
    total_length = get_duration(wav_file)
    time.sleep(total_length)
    
    
    # 返回收到的数据，这只是为了演示
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
 