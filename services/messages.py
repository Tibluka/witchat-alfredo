import json
import requests
from cryptography.fernet import Fernet



def sendMessage(message, API_KEY):
    headers = {"Authorization": API_KEY, "Content-Type": "application/json"}
    endpoint = 'https://api.openai.com/v1/completions'
    model = "text-davinci-003"
    payload = {
        "model": model,
        "prompt": message,
        "max_tokens": 1000
    }
    payload = json.dumps(payload)
    response = requests.post(endpoint, headers=headers, data=payload).json()
    m = response["choices"][0]["text"]
    return m
    