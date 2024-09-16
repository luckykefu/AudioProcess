import argparse
from src.update_xstudio_lrc import update_xstudio_lrc
from src.extract_text import extract_text
from src.lrc2srt import lrc2srt
from src.update_srt_with_new_subtitles import (
    update_srt_with_new_subtitles,
)
from src.log import logger
import gradio as gr


with gr.Blocks() as demo:
    with gr.TabItem("Audio"):
        with gr.TabItem("Audio2Text Whisper"):
            with gr.Row():
                audio_file_path5 = gr.Audio(label="上传音频文件", type="filepath")
                model_path = gr.Textbox(
                    label="模型路径", value="whisper_models/small.pt"
                )
                with gr.Row():
                    prompt = gr.Textbox(label="Prompt", value="", lines=2)
                    output_format = gr.Dropdown(
                        choices=["txt", "vtt", "srt", "tsv", "json", "all"],
                        label="输出格式",
                        value="all",
                    )
                    output_dir1 = gr.Textbox(label="输出文件夹", value="temp")
            with gr.Row():
                audio_recognition_btn = gr.Button("识别")

            gr.Markdown("### 文件在output文件夹下")
            with gr.Row():

                audio_recognition_output = gr.Textbox(
                    label="识别结果", lines=5, value=""
                )

            audio_recognition_btn.click(
                fn=audio2text,
                inputs=[
                    audio_file_path5,
                    model_path,
                    prompt,
                    output_format,
                    output_dir1,
                ],
                outputs=[audio_recognition_output],
            )

        with gr.TabItem("BPM"):
            audo_file_path2 = gr.File(label="上传音频文件", type="filepath")
            bpm_btn = gr.Button("RUN")
            with gr.Row():
                bpm_output = gr.Number(label="BPM")
                key_output = gr.Textbox(label="Key")
                mode_output = gr.Textbox(label="Mode")
            bpm_btn.click(
                fn=get_key_and_bpm,
                inputs=[audo_file_path2],
                outputs=[bpm_output, key_output, mode_output],
            )
        
        with gr.TabItem("音视频分离"):

            with gr.Row():
                video_file_path1 = gr.Video(label="上传视频文件", sources=["upload"])
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
                with gr.Row():
                    voice_gender = gr.Dropdown(
                        choices=["male", "female"], label="性别", value="female"
                    )
                    voice_itn = gr.Dropdown(
                        choices=get_edge_tts_voices_itn(),
                        label="国家",
                        value="",
                    )
                voice_dropdown = gr.Dropdown(
                    choices=get_edge_tts_voices(voice_gender.value, voice_itn.value),
                    label="声音选择",
                    value="",
                )
                voice_gender.change(
                    fn=get_edge_tts_voices,
                    inputs=[voice_gender, voice_itn],
                    outputs=[voice_dropdown],
                )
                voice_itn.change(
                    fn=get_edge_tts_voices,
                    inputs=[voice_gender, voice_itn],
                    outputs=[voice_dropdown],
                )
                rate_slider = gr.Slider(
                    minimum=-50, maximum=50, step=5, value=0, label="Rate (%)"
                )
                volume_slider = gr.Slider(
                    minimum=-50, maximum=50, step=5, value=0, label="Volume (%)"
                )
                output_dir3 = gr.Textbox(label="Output Dir", value="temp")
            with gr.Column():
                generate_button = gr.Button("Generate Audio")
            with gr.Column():
                audio_output = gr.Audio(label="Generated Audio")
            generate_button.click(
                fn=edge_tts_func,
                inputs=[
                    text_input2,
                    voice_dropdown,
                    rate_slider,
                    volume_slider,
                    output_dir3,
                ],
                outputs=audio_output,
            )

if __name__ == "__main__":
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
