import asyncio
import os
from typing import List
import edge_tts
from .log import get_logger

logger = get_logger(__name__)


async def get_edge_tts_voices() -> List[str]:
    """
    获取所有可用的 Edge TTS 声音。

    Returns:
    - List[str]: 所有可用声音的简短名称和性别组合。

    Raises:
    - Exception: 如果获取声音列表失败。
    """
    try:
        voices = await edge_tts.list_voices()
        return [f"{voice['ShortName']}_{voice['Gender']}" for voice in voices]
    except Exception as e:
        logger.error(f"Failed to get TTS voices: {e}")
        raise


async def edge_tts_func(text_input: str, voice_dropdown: str) -> str:
    """
    使用 Edge TTS 合成音频文件。

    Parameters:
    - text_input: 要合成的文本。
    - voice_dropdown: 选择的声音。

    Returns:
    - str: 输出文件的路径。

    Raises:
    - Exception: 如果音频生成失败。
    """
    try:
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{text_input[:10]}_output.mp3")

        logger.info(f"Generating TTS audio with voice {voice_dropdown}.")

        voice = voice_dropdown.split("_")[0]
        communicate = edge_tts.Communicate(text_input, voice)

        await communicate.save(output_file)

        logger.info(f"TTS audio saved to {output_file}.")
        return output_file

    except Exception as e:
        logger.error(f"Failed to generate TTS audio: {e}")
        raise


def run_edge_tts(text_input: str, voice: str) -> str:
    """
    异步函数的同步包装器。

    Parameters:
    - text_input: 要合成的文本。
    - voice: 选择的声音。
    - output_dir: 输出文件的目录。

    Returns:
    - str: 输出文件的路径。
    """
    return asyncio.run(edge_tts_func(text_input, voice))


if __name__ == "__main__":
    voices = asyncio.run(get_edge_tts_voices())
    print(f"Available voices: {len(voices)}")
    text_input = "Hello world"
    voice_dropdown = voices[0]
    output_file = run_edge_tts(text_input, voice_dropdown)
    print(f"TTS audio saved to {output_file}.")
