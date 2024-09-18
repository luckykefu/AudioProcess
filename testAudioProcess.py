# AudioProcess\TestAudioProcess.py
# --coding:utf-8--
# Time:2024-09-17 22:04:52
# Author:Luckykefu
# Email:3124568493@qq.com
# Description: Test cases for AudioProcess functionalities

import os
import unittest
from src.get_key_and_bpm import get_key_and_bpm
from src.extract_audio import extract_audio
from src.audio_clip import audio_clip
from src.edgeTTS import get_edge_tts_voices, edge_tts_func
import asyncio

# Get the absolute path of the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory
os.chdir(script_dir)

class TestAudioProcess(unittest.TestCase):

    # def test_get_key_and_bpm(self):
    #     audio_file = r"d:\Music\男孩 (Live)\男孩 (Live).flac"
    #     bpm, key, mode = get_key_and_bpm(audio_file)
    #     self.assertIsNotNone(bpm)
    #     self.assertIsNotNone(key)
    #     self.assertIsNotNone(mode)
    #     print(f"BPM: {bpm}, Key: {key}, Mode: {mode}")

    # def test_extract_audio(self):
    #     video_file = r"d:\Videos\060 云宫迅音\060.mp4"
    #     output_file = extract_audio(video_file)
    #     self.assertTrue(os.path.exists(output_file))
    #     print(f"Extracted audio file: {output_file}")

    def test_audio_clip(self):
        audio_file = r"d:\Music\红尘客栈 - 胖哥\Music_红尘客栈.flac"
        start_time = 10
        end_time = 20
        clipped_file = audio_clip(audio_file, start_time, end_time)
        self.assertTrue(os.path.exists(clipped_file))
        print(f"Clipped audio file: {clipped_file}")

    # def test_edge_tts(self):
    #     async def test_voices():
    #         voices = await get_edge_tts_voices()
    #         self.assertIsNotNone(voices)
    #         print(f"Available voices: {voices}")

    #     asyncio.run(test_voices())

    #     output_path = edge_tts_func("Hello world", "en-US-GuyNeural", "output")
    #     self.assertTrue(os.path.exists(output_path))
    #     print(f"Generated TTS audio file: {output_path}")

if __name__ == "__main__":
    unittest.main()
