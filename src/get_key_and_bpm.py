import os
import librosa
import numpy as np
from .log import get_logger

logger = get_logger(__name__)


def detect_bpm(audio_file):
    logger.info(f"Detecting BPM for {audio_file}")
    y, sr = librosa.load(audio_file, sr=None)
    # 动态计算 hop_length
    desired_time_shift_seconds = 0.001  # 相当于大约 25ms
    hop_length = int(desired_time_shift_seconds * sr)
    logger.info(f"Hop length: {hop_length}")
    # 计算起始强度
    onset_env = librosa.onset.onset_strength(
        y=y, sr=sr, hop_length=hop_length, aggregate=np.mean
    )
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    logger.info(f"BPM detected: {tempo[0]}")
    return tempo[0]


# 定义标准的大调和小调轮廓
MAJOR_PROFILE = np.array(
    [6.35, 2.23, 3.48, 2.01, 1.40, 4.32, 4.79, 2.52, 3.56, 2.31, 2.11, 0.50]
)

MINOR_PROFILE = np.array(
    [6.33, 2.69, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
)


def detect_key_krumhansl_schmuckler(chroma):
    """使用 Krumhansl-Schmuckler 算法检测音频的调性"""
    # 计算色度图的平均值
    chroma_mean = np.mean(chroma, axis=1)

    # 初始化最大相似度和对应的调性索引
    max_similarity = -float("inf")
    key_index = None
    key_type = None

    # 计算每个可能的调性与色度图之间的相似度
    for i in range(12):
        # 旋转轮廓以匹配当前调性
        rotated_major_profile = np.roll(MAJOR_PROFILE, i)
        rotated_minor_profile = np.roll(MINOR_PROFILE, i)

        # 计算相似度
        major_similarity = np.dot(chroma_mean, rotated_major_profile)
        minor_similarity = np.dot(chroma_mean, rotated_minor_profile)

        # 更新最大相似度和对应的调性索引
        if major_similarity > max_similarity:
            max_similarity = major_similarity
            key_index = i
            key_type = "Major"
        if minor_similarity > max_similarity:
            max_similarity = minor_similarity
            key_index = i
            key_type = "Minor"

    # 定义所有可能的调性名称
    keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    key_name = keys[key_index]

    return key_name, key_type


def detect_key(audio_file):
    """检测音频文件的调性"""
    logger.info(f"Detecting key for {audio_file}")

    try:
        if not os.path.exists(audio_file):
            logger.error(f"Audio file not found: {audio_file}")
            return None

        # 加载音频文件
        y, sr = librosa.load(audio_file)

        # 计算色度图
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

        # 使用 Krumhansl-Schmuckler 算法检测调性
        key_name, key_type = detect_key_krumhansl_schmuckler(chroma)

        logger.info(f"Key detected: {key_name} {key_type}")
        return key_name, key_type

    except librosa.ParameterError as pe:
        logger.error(f"Librosa parameter error: {pe}")
        return None, None
    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        return None, None


def get_key_and_bpm(audio_file):
    bpm = detect_bpm(audio_file)
    key_name, key_type = detect_key(audio_file)
    return bpm, key_name, key_type


# 测试代码
if __name__ == "__main__":
    audio_file = r"d:\Music\男孩 (Live)\男孩 (Live).flac"
    detect_bpm(audio_file)
    # detect_key(audio_file)
