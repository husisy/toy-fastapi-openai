import os
import time
import typing
import dotenv
import fastapi
import pydantic
import openai

dotenv.load_dotenv()

SIGNED_API_KEY = {str(x) for x in os.environ.get('SIGNED_API_KEY','').split(',') if x}
# python -c 'import secrets; print(secrets.token_urlsafe(24))'
openai.api_key = os.environ["OPENAI_API_KEY"]

class ChatGPTSentence(pydantic.BaseModel):
    role: str
    content: str

class ChatGPTConversation(pydantic.BaseModel):
    sentence: list[ChatGPTSentence]
    temperature: float = 0.6

app = fastapi.FastAPI()
# TODO system
@app.put("/multiround/{apikey}")
def update_item(apikey: str, chat: ChatGPTConversation):
    if apikey in SIGNED_API_KEY:
        tmp0 = chat.model_dump()['sentence']
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=tmp0, temperature=chat.temperature)
        ret = {'response': response.choices[0].message.content}
        return ret
    else:
        time.sleep(10)

class ChatGPTOneSentenceOnly(pydantic.BaseModel):
    inputMessage: str
    temperature: float = 0.6

@app.put("/oneround/{apikey}")
def update_item(apikey: str, message: ChatGPTOneSentenceOnly):
    if apikey in SIGNED_API_KEY:
        print(message)
        if message.inputMessage:
            tmp0 = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message.inputMessage},
            ]
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=tmp0, temperature=message.temperature)
            ret = {'replyMessage': response.choices[0].message.content,
                   'total_tokens': response["usage"]["total_tokens"],
                   'completion_tokens': response['usage']['completion_tokens']}
        else:
            ret = {'replyMessage': None, 'completion_tokens': 0}
        return ret
    else:
        time.sleep(10)

# uvicorn draft00:app --port 9803 --host 0.0.0.0
