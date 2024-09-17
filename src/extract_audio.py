import os
from moviepy.editor import VideoFileClip  # 确保安装了 moviepy 库
from src.log import get_logger

logger = get_logger(__name__)


def extract_audio(input_file):
    """
    Extracts the audio from the input file and saves it to the output file.

    :param input_file: Path to the input video file.
    :return: Paths to the temporary video and audio files.
    """
    try:
        # 确保输入文件存在
        if not os.path.exists(input_file):
            logger.error(f"The input file does not exist: {input_file}")
            raise FileNotFoundError("The input file does not exist.")

        # 加载视频文件
        logger.info(f"Loading video file: {input_file}")
        clip = VideoFileClip(input_file)

        # 分离音频
        logger.info("Extracting audio from the video...")
        audio = clip.audio

        # 移除音频
        logger.info("Creating video without audio...")
        video = clip.without_audio()

        # 创建临时文件夹
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            logger.info(f"Creating temp directory: {temp_dir}")
            os.makedirs(temp_dir)

        # 定义临时文件路径
        temp_video_path = os.path.join(temp_dir, "temp_video.mp4")
        temp_audio_path = os.path.join(temp_dir, "temp_audio.mp3")

        # 保存无音频的视频
        logger.info(f"Saving video without audio to: {temp_video_path}")
        video.write_videofile(temp_video_path, codec="libx264", audio_codec="aac")

        # 保存音频
        logger.info(f"Saving audio to: {temp_audio_path}")
        audio.write_audiofile(temp_audio_path, codec="libmp3lame")

        # 返回视频和音频的文件路径
        logger.info(f"Audio and video extracted successfully.")
        return temp_video_path, temp_audio_path

    except Exception as e:
        logger.error(f"An error occurred while extracting audio: {e}")
        raise
