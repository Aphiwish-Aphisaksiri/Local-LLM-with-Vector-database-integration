import requests

url = "http://localhost:8000/chat"
session_id = "test-session-1"
history = []

print("Type 'exit' to quit.")
while True:
    prompt = input("You: ")
    if prompt.strip().lower() == "exit":
        break
    data = {
        "prompt": prompt,
        "history": history,
        "session_id": session_id
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        answer = response.json().get("response", "(no response)")
        print("Assistant:", answer)
        # Add to history for context
        history.append({"user": prompt, "assistant": answer})
    else:
        print("Error:", response.status_code, response.text)
