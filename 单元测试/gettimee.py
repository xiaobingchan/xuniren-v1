import  librosa

# 获取wav时长
def get_duration(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None) # sr=None 保持原始采样率
        duration = librosa.get_duration(y=y, sr=sr)
        return duration
    except Exception as e:
        print(f"Error with librosa: {e}")
        return None