import json
import requests

def sendMessage(message, API_KEY):
    headers = {"Authorization": API_KEY, "Content-Type": "application/json"}
    endpoint = 'https://api.openai.com/v1/chat/completions'
    model = "gpt-3.5-turbo"
    payload = {
        "model": model,
        "messages": message
    }
    payload = json.dumps(payload)
    response = requests.post(endpoint, headers=headers, data=payload).json()
    m = None
    if response.get("id"):
        m = response["choices"][0]["message"]["content"]
    return m
    