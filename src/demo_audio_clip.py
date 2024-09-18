from .audio_clip import audio_clip
import gradio as gr


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
