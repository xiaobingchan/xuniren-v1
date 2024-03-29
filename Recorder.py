import sounddevice as sd
import soundfile as sf

import threading
import webrtcvad
import time
import io
import numpy as np
from scipy.io import wavfile as wf

class Recorder(object):
    
    def __init__(self, dtype='int16', channels=1, sample_rate=16000, chunk=1024) -> None:
        super().__init__()
        
        self.dtype = dtype
        self.channels = channels
        self.sample_rate = sample_rate
        self.chunk = chunk
        
        self.play_event = threading.Event()
        
        self.istream = sd.RawInputStream(samplerate=self.sample_rate, 
                                         blocksize=self.chunk,
                                         dtype=self.dtype,
                                         channels=self.channels,
                                         latency=0.1)
        print("Recorder initialized")
    
    def start(self):
        if self.istream.stopped:
            self.istream.start()
            self.get_record_audio(duration=100)
            print("* start recording")
        
    def stop(self):
        if self.istream.active:
            self.istream.stop()
            print("* stop recording")
        
    def abort(self):
        if self.istream.active:
            self.istream.abort()
            print('* abort recording')
        
    def get_record_audio(self, duration=1000):
        """获取固定时长的输入音频

        Args:
            duration (int, optional): 音频输入时长，单位为毫秒.. Defaults to 1000.

        Returns:
            bytes: raw 格式的输入音频
        """
        self.start()
            
        length = duration // 1000 * self.sample_rate
        frames = []
        for _ in range(0, max(int(length / self.chunk), 1)):
            data, overflowed = self.istream.read(self.chunk)
            frames.append(data)

        return b''.join(frames)
    
    def get_record_audio_with_len(self, frame_len):
        """获取固定大小的音频片段，注意 16bit 的采样精度返回的数据长度为 2 倍

        Args:
            frame_len (int): 音频采样数

        Returns:
            bytes: raw 格式的输入音频
        """
        # 因为采样率是 16bit，所以返回的长度其实是 frame_len * 2
        if self.istream.stopped:
            self.start()
        frames, overflowed = self.istream.read(frame_len)
        
        return frames
    
    def get_record_audio_with_vad(self, duration=10000, vad_bos=5000, vad_eos=2000, aggressiveness=3, filter_blank=True): 
        """获取音频，使用 vad 自动判断停止输入并截断

        Args:
            duration (int, optional): 最长输入音频时长，单位为毫秒. Defaults to 10000.
            vad_bos (int, optional): 允许的句首空白时长，单位为毫秒. Defaults to 5000.
            vad_eos (int, optional): 允许的句尾空白时长，单位为毫秒. Defaults to 2000.
            aggressiveness (int, optional): 过滤无声音频的强度，取值范围为整数 0~3. Defaults to 3.

        Returns:
            (bytes, bool): (raw 格式的输入音频, 是否有输入音频)
        """
        self.start()
        vad = webrtcvad.Vad(aggressiveness)
        bos_cnt = 0
        eos_cnt = 0
        frame_duration = 20
        frames = b''
        has_spoken = False
        
        for i in range(duration // frame_duration):
            #time.sleep(0.02)
            frame = self.get_record_audio_with_len(frame_len=self.sample_rate // 1000 * frame_duration)
            
            frames += frame
            if vad.is_speech(frame, self.sample_rate):
                has_spoken = True
                eos_cnt = 0
            else:
                if not has_spoken:
                    bos_cnt += frame_duration
                else:
                    eos_cnt += frame_duration
            if bos_cnt >= vad_bos:
                # 如果是句首空白停止，返回空串
                frames = b''
                break
            elif eos_cnt >= vad_eos:
                # 如果是句尾空白停止，停止录音并返回
                if filter_blank:
                    # 过滤句首句尾空白
                    pre_blank_len = bos_cnt * self.sample_rate // 1000
                    suf_blank_len = vad_eos * self.sample_rate // 1000
                    if self.dtype == 'int16':
                        pre_blank_len *= 2
                        suf_blank_len *= 2
                    frames = frames[pre_blank_len:-suf_blank_len]
                break
        self.abort()
        return frames, has_spoken
    
    def play_file(self, filename, blocking=True):
        """播放来自文件的内容

        Args:
            filename (str): 文件名
            blocking (bool): 播放时是否阻塞

        Raises:
            sd.CallbackStop: 停止播放的回调
        """

        data, samplerate = sf.read(filename, always_2d=True)
        sd.play(data, samplerate=samplerate, blocking=blocking)
        
    def play_buffer(self, buffer, sample_rate=16000, blocking=False):
        """播放内存中的数据

        Args:
            buffer (bytes): 要播放的数据, 存放在内存中
            sample_rate (int): 采样率
            blocking (bool): 播放时是否阻塞

        Raises:
            sd.CallbackStop: 停止播放的回调
        """
        audio = self.convert_bytearray_to_wav_ndarray(buffer, sample_rate=sample_rate)
        sd.play(audio, samplerate=sample_rate, blocking=blocking)
        
    def __del__(self):
        self.istream.stop()
        self.istream.close()
        
        print("Recorder deleted")
        return

    def convert_bytearray_to_wav_ndarray(self, input_bytearray: bytes, sample_rate=16000):
        """将音频流 bytes 转化为 numpy 的 ndarray

        Args:
            input_bytearray (bytes): 原始音频流
            sampling_rate (int, optional): 采样率. Defaults to 16000.

        Returns:
            ndarray: ndarray 格式的音频流
        """
        bytes_wav = bytes()
        byte_io = io.BytesIO(bytes_wav)
        wf.write(byte_io, sample_rate, np.frombuffer(input_bytearray, dtype=np.int16))
        output_wav = byte_io.read()
        output, samplerate = sf.read(io.BytesIO(output_wav))
        return output

    def save_audio(self, filename, raw_audio, sample_rate=16000):
        """保存音频流到指定文件中

        Args:
            filename (str): 音频文件名
            raw_audio (bytes): 原始音频流
            sample_rate (int, optional): 采样率. Defaults to 16000.
        """
        wav_audio = self.convert_bytearray_to_wav_ndarray(raw_audio, sample_rate=sample_rate)
        wf.write(filename, sample_rate, wav_audio)
        print("Save audio to %s" % filename)

if __name__ == '__main__':
    r = Recorder()
    frames, has_spoken = r.get_record_audio_with_vad(duration=10000)
    print(len(frames))