import os
import librosa
import numpy as np
from src.log import get_logger

logger = get_logger(__name__)


def detect_mode(chroma, key_index):
    """检测调式（大调或小调）"""
    # 获得大调和小调的模板
    major_template = np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1])
    minor_template = np.array([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])

    # 计算当前音调的 Chroma 特征
    chroma_mean = np.mean(chroma, axis=1)

    # 旋转模板以匹配当前的 key_index
    major_template = np.roll(major_template, key_index)
    minor_template = np.roll(minor_template, key_index)

    # 计算与大调和小调模板的相似度
    major_score = np.dot(chroma_mean, major_template)
    minor_score = np.dot(chroma_mean, minor_template)

    return "Major" if major_score > minor_score else "Minor"


def get_key_and_bpm(audio_file):
    """
    获取音频文件的 BPM 和 Key。

    :param audio_file: 音频文件的路径。
    :return: BPM, Key 名称, 调式
    """
    try:
        # 清理音频文件路径
        audio_file = audio_file.strip().replace('"', "").replace("'", "")

        # 检查音频文件是否存在
        if not os.path.exists(audio_file):
            logger.error(f"Audio file not found: {audio_file}")
            return None, None, None

        # 加载音频文件
        logger.info(f"Loading audio file: {audio_file}")
        y, sr = librosa.load(audio_file)

        # 检测 BPM
        logger.info("Detecting BPM...")
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

        # 检测 Key
        logger.info("Detecting Key and Mode...")
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        key_index = np.argmax(chroma_mean)
        keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        key = keys[key_index]
        mode = detect_mode(chroma, key_index)

        logger.info(f"BPM detected: {tempo[0]}, Key: {key}, Mode: {mode}")
        return tempo[0], key, mode

    except Exception as e:
        logger.error(f"An error occurred while processing the audio file: {e}")
        return None, None, None
