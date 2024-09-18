import os
from moviepy.editor import AudioFileClip
from src.log import get_logger

logger = get_logger(__name__)


def audio_clip(audio_file_path: str, start_time: float, end_time: float) -> str:
    """
    Crops the audio file from the start_time to the end_time.

    Parameters:
    - audio_file_path: str, the file path of the audio file to be cropped.
    - start_time: float, the start time in seconds for cropping.
    - end_time: float, the end time in seconds for cropping.

    Returns:
    - str, the file path of the cropped audio file.

    Raises:
    - FileNotFoundError: If the input audio file does not exist.
    - ValueError: If start_time or end_time is invalid.
    """
    if not os.path.exists(audio_file_path):
        logger.error(f"The input audio file does not exist: {audio_file_path}")
        raise FileNotFoundError(
            f"The input audio file does not exist: {audio_file_path}"
        )

    if start_time < 0 or end_time <= start_time:
        logger.error(
            f"Invalid start_time or end_time: start_time={start_time}, end_time={end_time}"
        )
        raise ValueError("start_time must be non-negative and less than end_time")

    logger.info(f"Loading audio file: {audio_file_path}")
    with AudioFileClip(audio_file_path) as clip:
        if end_time > clip.duration:
            logger.warning(
                f"end_time ({end_time}) exceeds clip duration ({clip.duration}). Adjusting to clip duration."
            )
            end_time = clip.duration

        logger.info(f"Cropping audio from {start_time} to {end_time} seconds.")
        cropped_clip = clip.subclip(start_time, end_time)

        temp_dir = os.path.join(os.path.dirname(audio_file_path), "temp")
        os.makedirs(temp_dir, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
        cropped_audio_filename = os.path.join(
            temp_dir, f"cropped_{base_name}_{start_time:.2f}_{end_time:.2f}.mp3"
        )

        logger.info(f"Writing cropped audio to: {cropped_audio_filename}")
        cropped_clip.write_audiofile(cropped_audio_filename, logger=None)

    logger.info("Cropped audio saved successfully.")
    return cropped_audio_filename


# Example usage:
# audio_file_path = "path/to/input_audio.mp3"
# start_time = 10.0  # Start time in seconds
# end_time = 20.0  # End time in seconds
# try:
#     cropped_audio_path = audio_clip(audio_file_path, start_time, end_time)
#     print(f"Cropped audio path: {cropped_audio_path}")
# except (FileNotFoundError, ValueError) as e:
#     print(f"Error: {e}")
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")
