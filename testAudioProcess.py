# AudioProcess\TestAudioProcess.py
# --coding:utf-8--
# Time:2024-09-17 22:04:52
# Author:Luckykefu
# Email:3124568493@qq.com
# Description: Test cases for AudioProcess functionalities

import os
import unittest
from src.get_key_and_bpm import *
from src.extract_audio import extract_audio
from src.audio_clip import audio_clip
from src.edgeTTS import get_edge_tts_voices, edge_tts_func, run_edge_tts
import asyncio

# Get the absolute path of the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory
os.chdir(script_dir)

# 测试代码
# if __name__ == "__main__":
#     audio_file = r"d:\Music\男孩 (Live)\男孩 (Live).flac"
#     bpm, key, mode = get_key_and_bpm(audio_file)
#     print(bpm, key, mode)

if __name__ == "__main__":
    voices = asyncio.run(get_edge_tts_voices())
    print(f"Available voices: {len(voices)}")
    text_input = "Hello world"
    voice_dropdown = voices[0]
    output_file = run_edge_tts(text_input, voice_dropdown)
    print(f"TTS audio saved to {output_file}.")