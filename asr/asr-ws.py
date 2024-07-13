# Real-time speech recognition from a microphone with sherpa-ncnn Python API
# with endpoint detection.
#
# Please refer to
# https://k2-fsa.github.io/sherpa/ncnn/pretrained_models/index.html
# to download pre-trained models

# pip install websockets
# pip install pypinyin -i https://mirrors.aliyun.com/pypi/simple

import sys
import asyncio
import websockets
import json
import re
import pypinyin
from pypinyin import Style

def get_fuzzy_pinyin(text):
    """
    获取中文字符串text的模糊拼音码
    """
    # 将中文字符串转换为拼音列表
    pinyin_list = pypinyin.lazy_pinyin(text, style=Style.NORMAL)
    # 将拼音列表连接成字符串
    fuzzy_pinyin = ''.join(pinyin for py in pinyin_list for pinyin in py)
    return fuzzy_pinyin

def match_fuzzy_pinyin(text, pinyin_str):
    """
    判断中文字符串text的拼音是否与pinyin_str模糊匹配
    """
    # 将中文字符串转换为拼音列表
    pinyin_list = pypinyin.lazy_pinyin(text)
    # 构造正则表达式模式
    patterns = [
        '.*'.join(['', 'xiao', 'hong','xiao','hong', ''])
    ]
    # 判断拼音字符串是否模糊匹配
    return any(re.match(pattern, pinyin_str, re.IGNORECASE) for pattern in patterns)

def match_fuzzy_pinyin_v2(text, pinyin_str):
    """
    判断中文字符串text的拼音是否与pinyin_str模糊匹配
    """
    # 将中文字符串转换为拼音列表
    pinyin_list = pypinyin.lazy_pinyin(text)
    # 构造正则表达式模式
    patterns = [
        '.*'.join(['', 'xiao','hong', 'ni', 'hao', ''])
    ]
    # 判断拼音字符串是否模糊匹配
    return any(re.match(pattern, pinyin_str, re.IGNORECASE) for pattern in patterns)


async def send_message_to_websocket(message):
    async with websockets.connect('ws://localhost:60001') as websocket:
        await websocket.send(message)  # 发送消息给服务器
        print("Message sent")

def send_message(message):
    asyncio.run(send_message_to_websocket(message))

try:
    import sounddevice as sd
except ImportError as e:
    print("Please install sounddevice first. You can use")
    print()
    print("  pip install sounddevice")
    print()
    print("to install it")
    sys.exit(-1)

import sherpa_ncnn

# 设置状态变量
is_listening = False
question_queue = []

def create_recognizer():
    # Please replace the model files if needed.
    # See https://k2-fsa.github.io/sherpa/ncnn/pretrained_models/index.html
    # for download links.
    recognizer = sherpa_ncnn.Recognizer(
        tokens="./tokens.txt",
        encoder_param="./encoder_jit_trace-pnnx.ncnn.param",
        encoder_bin="./encoder_jit_trace-pnnx.ncnn.bin",
        decoder_param="./decoder_jit_trace-pnnx.ncnn.param",
        decoder_bin="./decoder_jit_trace-pnnx.ncnn.bin",
        joiner_param="./joiner_jit_trace-pnnx.ncnn.param",
        joiner_bin="./joiner_jit_trace-pnnx.ncnn.bin",
        num_threads=4,
        decoding_method="modified_beam_search",
        enable_endpoint_detection=True,
        rule1_min_trailing_silence=2.4,
        rule2_min_trailing_silence=1.2,
        rule3_min_utterance_length=300,
        hotwords_file="",
        hotwords_score=1.5,
    )
    return recognizer


def main():
    print("开始识别，请说话")
    recognizer = create_recognizer()
    sample_rate = recognizer.sample_rate
    samples_per_read = int(0.1 * sample_rate)  # 0.1 second = 100 ms
    last_result = ""
    segment_id = 0

    with sd.InputStream(channels=1, dtype="float32", samplerate=sample_rate) as s:
        while True:
            samples, _ = s.read(samples_per_read)  # a blocking read
            samples = samples.reshape(-1)
            recognizer.accept_waveform(sample_rate, samples)

            is_endpoint = recognizer.is_endpoint

            result = recognizer.text
            if result and (last_result != result):
                last_result = result
                #print("\r{}:{}".format(segment_id, result), end="", flush=True)

            if is_endpoint:
                if result:
                    print("\r{}:{}".format(segment_id, result), flush=True)
                    global is_listening
                    text=result
                    fuzzy_pinyin = get_fuzzy_pinyin(text)
                    #if "小智小智" in str(text.lower()):
                    if match_fuzzy_pinyin(text, fuzzy_pinyin):
                        is_listening = True
                        print("唤醒数字人...")
                        my_dict = {
                            "type": "nihao",
                            "content": "你好我在"
                        }
                        json_string = json.dumps(my_dict, ensure_ascii=False)
                        result = json_string
                        print("ws 60001发送数据："+result)
                        send_message(result)
                    
                    elif "停止" in text:
                        is_listening = True
                        print("停止说话...")
                        my_dict = {
                            "type": "stop",
                            "content": "你好我在"
                        }
                        json_string = json.dumps(my_dict, ensure_ascii=False)
                        result = json_string
                        print("ws 60001发送数据："+result)
                        send_message(result)
                    

                    elif is_listening and "你好我在" not in text and not match_fuzzy_pinyin_v2(text, fuzzy_pinyin) and "您好我在" not in text and "我在" not in text  and "初始" not in text:
                        is_listening = False
                        
                        if "换装" in text:
                            print("换装...")
                            my_dict = {
                                "type": "huanzhuang",
                                "content": ""
                            }
                            json_string = json.dumps(my_dict, ensure_ascii=False)
                            result = json_string
                            print("ws 60001发送数据："+result)
                            send_message(result)
                        else:
                            print(f"提问文心一言: {text}")
                            if "介绍" in str(text) and "实验室" in str(text):
                                my_dict = {"type": "jieshao","url": "http://127.0.0.1/web/#/?id=0","content":"","delay":120}
                            else:
                                my_dict = {
                                    "type": "tiwen",
                                    "content": text
                                }
                            json_string = json.dumps(my_dict, ensure_ascii=False)
                            result = json_string
                            print("ws 60001发送数据："+result)
                            send_message(result)

                    result=""
                    segment_id += 1
                recognizer.reset()


if __name__ == "__main__":
    devices = sd.query_devices()
    #print(devices)
    default_input_device_idx = sd.default.device[0]
    #print(f'Use default device: {devices[default_input_device_idx]["name"]}')

    try:
        main()
    except KeyboardInterrupt:
        print("\nCaught Ctrl + C. Exiting")