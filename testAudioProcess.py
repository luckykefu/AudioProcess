# AudioProcess\TestAudioProcess.py
# --coding:utf-8--
# Time:2024-09-17 22:04:52
# Author:Luckykefu
# Email:3124568493@qq.com
# Description:

import os

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 更改当前工作目录
os.chdir(script_dir)

#####################################
# TODO: get_key_and_bpm

# from src.get_key_and_bpm import get_key_and_bpm

# if __name__ == '__main__':
#         # 示例调用
#     audio_file = r"d:\Music\男孩 (Live)\男孩 (Live).flac"
#     bpm, key, mode = get_key_and_bpm(audio_file)
#     print(f"BPM: {bpm}, Key: {key}, Mode: {mode}")

###############################################
# TODO: extract_audio

# from src.extract_audio import extract_audio
# if __name__ == '__main__':
#     # 示例调用
#     audio_file = r"d:\Videos\060 云宫迅音\060.mp4"
#     extract_audio(audio_file)

###########################################
# TODO: audio clip

# from src.audio_clip import audio_clip
# if __name__ == '__main__':
#     # 示例调用
#     audio_file = r"d:\Music\红尘客栈 - 胖哥\Music_红尘客栈.flac"
#     start_time = 10
#     end_time = 20
#     audio_clip(audio_file, start_time, end_time)

############################################
# TODO: edgetts
from src.edgeTTS import *

# if __name__ == "__main__":
#     voices =asyncio.run( get_edge_tts_voices())
#     print(voices)

if __name__ == "__main__":
    
    # 合成音频文件
    output_path =  edge_tts_func("Hello world", "en-US-GuyNeural_Male", "output")
    print(f"Output file path: {output_path}")

    
