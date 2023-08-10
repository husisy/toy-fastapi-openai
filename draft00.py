import os
import time
import typing
import dotenv
import fastapi
import pydantic
import openai

dotenv.load_dotenv()

_SIGNED_API_KEY = {str(x) for x in os.environ.get('SIGNED_API_KEY','').split(',') if x}
# python -c 'import secrets; print(secrets.token_urlsafe(24))'
openai.api_key = os.environ["OPENAI_API_KEY"]

class ChatGPTSentence(pydantic.BaseModel):
    role: str
    content: str

class ChatGPTConversation(pydantic.BaseModel):
    sentence: list[ChatGPTSentence]
    temperature: float = 0.6

app = fastapi.FastAPI()

@app.put("/doge/{apikey}")
def update_item(apikey: str, chat: ChatGPTConversation):
    if apikey in _SIGNED_API_KEY:
        tmp0 = chat.model_dump()['sentence']
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=tmp0, temperature=chat.temperature)
        ret = {'response': response.choices[0].message.content}
        return ret
    else:
        time.sleep(10)

# uvicorn draft00:app --port 9803
