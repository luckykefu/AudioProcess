# AudioProcessWebUI.py
# --coding:utf-8--
# Time:2024-09-17 22:04:52
# Author:Luckykefu
# Email:3124568493@qq.com
# Description:

import gradio as gr
import argparse

import os
from src.demo_split_audio_and_video import demo_split_audio_and_video
from src.demo_BPM import demo_BPM
from src.demo_audio_clip import demo_audio_clip
from src.demo_edgeTTS import demo_edge_tts
from src.edgeTTS import *
from src.log import get_logger

logger = get_logger(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def parse_arguments():

    # Parse command line arguments.
    parser = argparse.ArgumentParser(description=f"{__file__}")
    parser.add_argument(
        "--server_name", type=str, default="localhost", help="Server name"
    )
    parser.add_argument("--server_port", type=int, default=None, help="Server port")
    parser.add_argument("--root_path", type=str, default=None, help="Root path")
    return parser.parse_args()


def main():
    args = parse_arguments()
    with gr.Blocks() as demo:
        with gr.TabItem("BPM"):
            demo_BPM()
        with gr.TabItem("Split Audio and Video"):
            demo_split_audio_and_video()
        with gr.TabItem("Audio Clip"):
            demo_audio_clip()
        with gr.TabItem("edge-tts"):
            demo_edge_tts()

    demo.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        root_path=args.root_path,
        show_api=False,
    )
    logger.info(f"Starting server on {args.server_name}:{args.server_port}")


if __name__ == "__main__":
    main()
