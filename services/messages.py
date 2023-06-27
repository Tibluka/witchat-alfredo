import json
import requests
from api_key import API_KEY


def sendMessage(message):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    endpoint = 'https://api.openai.com/v1/chat/completions'
    model = "gpt-3.5-turbo"
    payload = {
        "model": model,
        "messages":[
            {"role": "user", "content": message}
        ]
    }
    payload = json.dumps(payload)
    response = requests.post(endpoint, headers=headers, data=payload).json()
    m = response["choices"][0]["message"]["content"]
    return m
    