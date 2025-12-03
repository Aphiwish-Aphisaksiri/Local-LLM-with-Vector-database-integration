from llama_cpp import Llama

MODEL_PATH = "models/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"  # Update path if needed

llm = Llama(model_path=MODEL_PATH, n_ctx=2048)

print("Type 'exit' to quit.")
while True:
    user_input = input("User: ")
    if user_input.strip().lower() == "exit":
        break
    prompt = f"<|user|> {user_input}\n<|assistant|>"
    output = llm(prompt, max_tokens=256, stop=["<|user|>", "<|assistant|>"])
    print("Assistant:", output["choices"][0]["text"].strip())
