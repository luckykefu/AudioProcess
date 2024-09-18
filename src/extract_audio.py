import os
from moviepy.editor import VideoFileClip
from .log import get_logger

logger = get_logger(__name__)


def extract_audio(input_file: str) -> tuple[str, str]:
    """
    Extracts the audio from the input video file and saves it separately.

    Args:
        input_file (str): Path to the input video file.

    Returns:
        tuple[str, str]: Paths to the temporary video (without audio) and audio files.

    Raises:
        FileNotFoundError: If the input file does not exist.
        Exception: For any other errors during the extraction process.
    """
    if not os.path.exists(input_file):
        logger.error(f"Input file does not exist: {input_file}")
        raise FileNotFoundError(f"Input file does not exist: {input_file}")

    logger.info(f"Processing video file: {input_file}")

    try:
        with VideoFileClip(input_file) as clip:
            temp_dir = "temp"
            os.makedirs(temp_dir, exist_ok=True)

            temp_video_path = os.path.join(temp_dir, "temp_video.mp4")
            temp_audio_path = os.path.join(temp_dir, "temp_audio.mp3")

            logger.info("Extracting and saving audio...")
            clip.audio.write_audiofile(temp_audio_path, codec="libmp3lame")

            logger.info("Saving video without audio...")
            clip.without_audio().write_videofile(temp_video_path, codec="libx264", audio_codec="aac")

        logger.info("Audio and video extracted successfully.")
        return temp_video_path, temp_audio_path

    except Exception as e:
        logger.error(f"Error during audio extraction: {str(e)}")
        raise

if __name__ == "__main__":
    input_file = r"d:\Videos\055 按河桥\55.mp4"
    extract_audio(input_file)