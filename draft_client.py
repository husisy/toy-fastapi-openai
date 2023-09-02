import os
import dotenv
import json
import requests

dotenv.load_dotenv()

FASTAPI_KEY = [x for x in os.environ['SIGNED_API_KEY'].split(',') if x][0]
SERVER_IP = os.environ['SERVER_IP']
SERVER_PORT = 9803

def hf_fastapi_chatgpt(sentence, temperature=0.3):
    headers = {'Authorization': f'Bearer {FASTAPI_KEY}', 'Content-Type': 'application/json', 'accept':'application/json'}
    data = {'sentence': sentence, 'temperature':temperature}
    if isinstance(sentence, str):
        url = f'http://{SERVER_IP}:{SERVER_PORT}/gpt/oneround'
    else:
        url = f'http://{SERVER_IP}:{SERVER_PORT}/gpt/multiround'
    ret = requests.get(url, data=json.dumps(data), headers=headers).json()
    return ret


def demo_gpt_multiround():
    sentence = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "hi."},
    ]
    print(hf_fastapi_chatgpt(sentence, temperature=0.3))


def demo_gpt_one_round():
    sentence = 'hi.'
    print(hf_fastapi_chatgpt(sentence, temperature=0.3))
