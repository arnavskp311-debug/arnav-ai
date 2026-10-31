import os
import gradio as gr
from huggingface_hub import InferenceClient

# Free Serverless 1.7B Model
MODEL_NAME = "HuggingFaceTB/SmolLM2-1.7B-Instruct"

# Hugging Face token from environment variables
HF_TOKEN = os.environ.get("HF_TOKEN", "")

client = InferenceClient(api_key=HF_TOKEN if HF_TOKEN else None)

SYSTEM_PROMPT = (
    "You are an intelligent, friendly personal AI assistant created by Arnav Sharma of class XI-D. "
    "When introducing yourself, greeting a user, or when asked who created or made you, always state: "
    "'Hello! I am an AI assistant created by Arnav Sharma of class XI-D.' "
    "Answer all user questions clearly, accurately, and politely."
)

def respond(message, history):
    if not message.strip():
        return ""

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Format conversation history
    if history:
        for item in history:
            if isinstance(item, dict):
                role = item.get("role", "user")
                content = item.get("content", "")
                if content:
                    messages.append({"role": role, "content": content})
            elif isinstance(item, (list, tuple)) and len(item) == 2:
                messages.append({"role": "user", "content": str(item[0])})
                messages.append({"role": "assistant", "content": str(item[1])})

    messages.append({"role": "user", "content": message.strip()})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=350,
            temperature=0.6,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to neural engine: {str(e)}. Please check that HF_TOKEN is configured."

demo = gr.ChatInterface(
    fn=respond,
    title="🤖 Personal AI Assistant",
    description="Created by Arnav Sharma of Class XI-D. Powered by a 1.7B neural model.",
    examples=["Who are you?", "Who created you?", "Write a Python script to sort a list", "How do I make tea?"],
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
