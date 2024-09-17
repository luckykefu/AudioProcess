import asyncio
import os
import edge_tts
from src.log import get_logger

logger = get_logger(__name__)


async def get_edge_tts_voices():
    """
    根据性别和语言筛选 Edge TTS 的声音。

    Parameters:
    - gender: str, 性别（male 或 female）。
    - lang: str, 语言（如 en-US）。

    Returns:
    - List[str]: 筛选后的声音短名称和性别组合。
    """
    try:
        voices = voices = await edge_tts.list_voices()
        filtered_voices = voices
        return [f"{voice['ShortName']}_{voice['Gender']}" for voice in filtered_voices]
    except Exception as e:
        logger.error(f"Failed to filter TTS voices: {e}")
        raise


def edge_tts_func(text_input, voice_dropdown, output_dir):
    """
    使用 Edge TTS 合成音频文件。

    Parameters:
    - text_input: str, 要合成的文本。
    - voice_dropdown: str, 选择的声音。
    - rate_slider: int, 语速调整百分比。
    - volume_slider: int, 音量调整百分比。
    - output_dir: str, 输出文件的目录。

    Returns:
    - str: 输出文件的路径。
    """
    try:
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)

        # 定义输出文件路径
        output_file = os.path.join(output_dir, f"{text_input[:10]}_output.mp3")

        logger.info(f"Generating TTS audio with voice {voice_dropdown}.")

        voice = voice_dropdown.split("_")[0]

        communicate = edge_tts.Communicate(
            text_input,
            voice,
        )

        # 异步保存音频文件
        asyncio.run(communicate.save(output_file))

        logger.info(f"TTS audio saved to {output_file}.")
        return output_file

    except Exception as e:
        logger.error(f"Failed to generate TTS audio: {e}")
        raise
