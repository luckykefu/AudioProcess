import os
from moviepy.editor import AudioFileClip
from src.log import logger


def audio_clip(audio_file_path, start_time, end_time):
    """
    Crops the audio file from the start_time to the end_time.

    Parameters:
    - audio_file_path: str, the file path of the audio file to be cropped.
    - start_time: float, the start time in seconds for cropping.
    - end_time: float, the end time in seconds for cropping.

    Returns:
    - str, the file path of the cropped audio file.
    """
    try:
        # 确保输入文件存在
        if not os.path.exists(audio_file_path):
            logger.error(f"The input audio file does not exist: {audio_file_path}")
            raise FileNotFoundError("The input audio file does not exist.")

        # 加载音频文件
        logger.info(f"Loading audio file: {audio_file_path}")
        clip = AudioFileClip(audio_file_path)

        # 裁剪音频
        logger.info(f"Cropping audio from {start_time} to {end_time} seconds.")
        cropped_clip = clip.subclip(start_time, end_time)

        # 创建临时文件夹
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            logger.info(f"Creating temp directory: {temp_dir}")
            os.makedirs(temp_dir)

        # 定义裁剪后音频的文件路径
        cropped_audio_filename = os.path.join(temp_dir, "cropped_audio.mp3")

        # 写入裁剪后的音频到文件
        logger.info(f"Writing cropped audio to: {cropped_audio_filename}")
        cropped_clip.write_audiofile(cropped_audio_filename)

        # 释放资源
        cropped_clip.close()

        # 返回裁剪后的音频文件路径
        logger.info(f"Cropped audio saved successfully.")
        return cropped_audio_filename

    except Exception as e:
        logger.error(f"An error occurred while cropping the audio: {e}")
        raise


# 示例调用
# audio_file_path = "path/to/input_audio.mp3"
# start_time = 10.0  # 起始时间，单位秒
# end_time = 20.0  # 结束时间，单位秒
# cropped_audio_path = audio_clip(audio_file_path, start_time, end_time)
# print(f"Cropped audio path: {cropped_audio_path}")
