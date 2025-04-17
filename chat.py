import time
import gradio as gr
from openai import OpenAI
# import openai

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY')
NVIDIA_MODEL = os.getenv('NV_MODEL')

def generate_response(message, history):
    
    """
    Function to stream OpenAI responses.
    """
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = NVIDIA_API_KEY
    )

    # Prepare the messages in the required format
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    for msg in history:
        if 'role' in msg:
            if msg['role'] == 'user':
                messages.append({"role": "user", "content": msg['content']})
            if msg['role'] == 'assistant':
                messages.append({"role": "assistant", "content": msg['content']})
    
    # Add the current user message to the conversation history if it's not empty
    if message and message.strip():
        messages.append({"role": "user", "content": message})

    # Call OpenAI's API with streaming enabled
    # meta/llama-3.3-70b-instruct
    completion = client.chat.completions.create(
        model=NVIDIA_MODEL,
        messages=messages,
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )

    # Stream the response chunks
    bot_message = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            bot_message += chunk.choices[0].delta.content
            yield history + [{"role": "assistant", "content": bot_message}]


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox(label="Your Message")
    clear = gr.Button("Clear Chat")

    def user_input(user_message, history):
        return "", history + [{"role": "user", "content": user_message}]

    # Link the user input and bot response functions
    msg.submit(user_input, [msg, chatbot], [msg, chatbot], queue=False).then(
        generate_response, inputs=[msg, chatbot], outputs=chatbot
    )
    
    # Clear button functionality
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch(share=False)
