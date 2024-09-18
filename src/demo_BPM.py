from .get_key_and_bpm import get_key_and_bpm
import gradio as gr


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
