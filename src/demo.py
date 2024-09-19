import gradio as gr
import asyncio
from .audio_clip import audio_clip
from .get_key_and_bpm import get_key_and_bpm
from .edgeTTS import get_edge_tts_voices, run_edge_tts
from .extract_audio import extract_audio


def demo_audio_clip():
    with gr.Blocks() as audio_clip_demo:
        gr.Markdown(f"## Audio Clip")
        audio_file = gr.Audio(label="Upload Audio File", type="filepath")
        start_time = gr.Number(label="开始时间", value=0)
        end_time = gr.Number(label="结束时间", value=10)
        audio_output = gr.Audio(label="裁剪后的音频", type="filepath")
        audio_clip_btn = gr.Button("RUN")
        audio_clip_btn.click(
            fn=audio_clip,
            inputs=[audio_file, start_time, end_time],
            outputs=[audio_output],
        )
    return audio_clip_demo


def demo_BPM():
    with gr.Blocks() as BPM_demo:
        gr.Markdown(f"## Get BPM and Key")
        audio_file = gr.Audio(label="Upload Audio File", type="filepath")
        bpm_btn = gr.Button("RUN")
        with gr.Row():
            bpm = gr.Number(label="BPM")
            key = gr.Textbox(label="Key")
            mode = gr.Textbox(label="Mode")
        bpm_btn.click(
            fn=get_key_and_bpm,
            inputs=[audio_file],
            outputs=[bpm, key, mode],
        )
    return BPM_demo


def demo_edge_tts():
    with gr.Blocks() as edge_tts_demo:
        gr.Markdown(f"## edge-tts")
        text_input = gr.Textbox(
            label="输入文本", lines=2, value="你好，欢迎使用 EDGETTS！"
        )

        with gr.Column():
            VOICE_CHOICES = asyncio.run(get_edge_tts_voices())

            voice = gr.Dropdown(
                choices=VOICE_CHOICES,
                label="声音选择",
                value=VOICE_CHOICES[0],
                allow_custom_value=True,
            )
        with gr.Column():
            generate_button = gr.Button("Generate Audio")
        with gr.Column():
            audio_output = gr.Audio(label="Generated Audio")
        generate_button.click(
            fn=run_edge_tts,
            inputs=[text_input, voice],
            outputs=audio_output,
            queue=True,  # 可选
        )

    return edge_tts_demo


def demo_split_audio_and_video():
    with gr.Blocks() as split_audio_and_video_demo:
        gr.Markdown(f"## Split Audio and Video")
        video_file = gr.Video(label="Upload Video File", sources=["upload"])
        extract_audio_btn = gr.Button("RUN")
        video_output = gr.Video(label="Extracted Video")
        audio_output = gr.Audio(label="Extracted Audio")
        extract_audio_btn.click(
            fn=extract_audio,
            inputs=[video_file],
            outputs=[video_output, audio_output],
        )
    return split_audio_and_video_demo
