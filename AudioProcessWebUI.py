# AudioProcessWebUI.py
# --coding:utf-8--
# Time:2024-09-17 22:04:52
# Author:Luckykefu
# Email:3124568493@qq.com
# Description:

import gradio as gr
import argparse

import os
from src.audio_clip import audio_clip
from src.extract_audio import extract_audio
from src.get_key_and_bpm import get_key_and_bpm
from src.edgeTTS import *
from src.log import get_logger

logger = get_logger(__name__)

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 更改当前工作目录
os.chdir(script_dir)
output_dir = os.path.join(script_dir, "output")


def main():

    # Define the interface
    with gr.Blocks() as demo:
        with gr.TabItem("AudioProcess"):
            with gr.TabItem("BPM"):
                audio_file_path2 = gr.File(label="上传音频文件", type="filepath")
                bpm_btn = gr.Button("RUN")
                with gr.Row():
                    bpm_output = gr.Number(label="BPM")
                    key_output = gr.Textbox(label="Key")
                    mode_output = gr.Textbox(label="Mode")
                bpm_btn.click(
                    fn=get_key_and_bpm,
                    inputs=[audio_file_path2],
                    outputs=[bpm_output, key_output, mode_output],
                )

            with gr.TabItem("音视频分离"):
                with gr.Row():
                    video_file_path1 = gr.Video(
                        label="上传视频文件", sources=["upload"]
                    )
                    extract_audio_btn = gr.Button("RUN")
                    video_output = gr.Video(label="提取的视频")
                    audio_output_path1 = gr.Audio(label="提取的音频")

                extract_audio_btn.click(
                    fn=extract_audio,
                    inputs=[video_file_path1],
                    outputs=[video_output, audio_output_path1],
                )

            with gr.TabItem("音频裁剪"):
                with gr.Row():
                    audio_file_path3 = gr.Audio(label="上传音频文件", type="filepath")
                    start_time = gr.Number(label="开始时间", value=0)
                    end_time = gr.Number(label="结束时间", value=10)
                    audio_output_path2 = gr.Audio(label="裁剪后的音频", type="filepath")
                    audio_cut_btn = gr.Button("RUN")

                audio_cut_btn.click(
                    fn=audio_clip,
                    inputs=[audio_file_path3, start_time, end_time],
                    outputs=[audio_output_path2],
                )

            with gr.TabItem("TXT2Audio edge-tts"):
                with gr.Row():
                    text_input2 = gr.Textbox(
                        label="输入文本", lines=4, value="你好，欢迎使用 EDGETTS！"
                    )

                with gr.Column():
                    VOICE_CHOICES = asyncio.run(get_edge_tts_voices())

                    voice_dropdown = gr.Dropdown(
                        choices=VOICE_CHOICES,
                        label="声音选择",
                        value=VOICE_CHOICES[0],
                        allow_custom_value=True,
                    )
                    output_dir3 = gr.Textbox(label="Output Dir", value=output_dir)
                with gr.Column():
                    generate_button = gr.Button("Generate Audio")
                with gr.Column():
                    audio_output = gr.Audio(label="Generated Audio")
                generate_button.click(
                    fn=edge_tts_func,
                    inputs=[
                        text_input2,
                        voice_dropdown,
                        output_dir3,
                    ],
                    outputs=audio_output,
                    queue=True,  # 可选
                )

    # Launch the interface
    parser = argparse.ArgumentParser(description="Demo")
    parser.add_argument(
        "--server_name", type=str, default="localhost", help="server name"
    )
    parser.add_argument("--server_port", type=int, default=8080, help="server port")
    parser.add_argument("--root_path", type=str, default=None, help="root path")
    args = parser.parse_args()

    demo.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        root_path=args.root_path,
        show_api=False,
    )


if __name__ == "__main__":
    main()
