from .edgeTTS import get_edge_tts_voices, run_edge_tts
import gradio as gr
import asyncio


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
