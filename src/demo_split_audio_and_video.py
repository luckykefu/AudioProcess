from .extract_audio import extract_audio
import gradio as gr


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
