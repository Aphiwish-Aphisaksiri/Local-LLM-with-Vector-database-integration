# Python LLM Chat Setup Guide (Windows)

This guide will help you set up and chat with a local LLM using Python. We'll use the `llama-cpp-python` library and a small GGUF model (e.g., TinyLlama).

## 1. Install Python and llama-cpp-python
- Make sure you have Python 3.8+ installed. Download from https://www.python.org/downloads/ if needed.
- Open `cmd.exe` and run:
  ```cmd
  pip install llama-cpp-python
  ```

## 2. Download a Small GGUF Model
- Visit: https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF
- Download a file like `TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf`.
- Place it in your project folder, e.g., `e:\.Homeworks\Life CH1\Code\LLM\models` (create the folder if needed).

## 3. Python Chat Script Example
Create a file named `chat_llm.py` in your project folder with the following content:

```python
from llama_cpp import Llama

# Path to your GGUF model
MODEL_PATH = "models/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"

llm = Llama(model_path=MODEL_PATH, n_ctx=2048)

print("Type 'exit' to quit.")
while True:
    user_input = input("User: ")
    if user_input.strip().lower() == "exit":
        break
    prompt = f"<|user|> {user_input}\n<|assistant|>"
    output = llm(prompt, max_tokens=256, stop=["<|user|>", "<|assistant|>"])
    print("Assistant:", output["choices"][0]["text"].strip())
```

## 4. Run the Chat
- In `cmd.exe`, navigate to your project folder:
  ```cmd
  cd /d e:\.Homeworks\Life CH1\Code\LLM
  ```
- Run the script:
  ```cmd
  python chat_llm.py
  ```
- Start chatting! Type your message and press Enter. Type `exit` to quit.

---
For more details, see: https://github.com/abetlen/llama-cpp-python
