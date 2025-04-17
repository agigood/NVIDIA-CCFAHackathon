import gradio as gr

css = """
.blue-text textarea {
    color: red !important;
}
"""


with gr.Blocks(css=css) as demo:
    with gr.Column():
        with gr.Row():
            text_input1 = gr.Textbox(label="Enter your text 1", elem_classes="blue-text")
            text_input2 = gr.Textbox(label="Enter your text 2")
        text_output = gr.Textbox(label="Output", interactive=False)
        color_selection = gr.Dropdown(
            choices=["Red", "Green", "Blue"],
            label="Select a color",
            interactive=True
        )
        submit_btn = gr.Button("Submit")

        def update_output(text1, text2):
            return text1+' : '+text2

        submit_btn.click(
            fn=update_output,
            inputs=[text_input1, text_input2],
            outputs=text_output
        )

demo.launch(share=False)
