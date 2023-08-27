import os
import dotenv
import json
import requests

dotenv.load_dotenv()

_FASTAPI_KEY = [x for x in os.environ['SIGNED_API_KEY'].split(',') if x][0]
_SERVER_IP = os.environ['SERVER_IP']
_SERVER_PORT = 9803

def hf_fastapi_chatgpt(sentence, temperature=0.3):
    data = {'sentence': sentence, 'temperature':temperature}
    headers = {'Content-Type': 'application/json', 'accept':'application/json'}
    url = f'http://{_SERVER_IP}:{_SERVER_PORT}/multiround/{_FASTAPI_KEY}'
    response = requests.put(url, data=json.dumps(data), headers=headers)
    ret = response.json()['response']
    return ret

sentence = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "hi."},
]
print(hf_fastapi_chatgpt(sentence, temperature=0.3))
