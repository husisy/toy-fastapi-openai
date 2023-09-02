import os
import time
import typing
import dotenv
import fastapi
import pydantic
import openai

dotenv.load_dotenv()

SIGNED_API_KEY = {str(x) for x in os.environ.get('SIGNED_API_KEY','').split(',') if x}
# python -c 'import secrets; print(secrets.token_hex(32))'
openai.api_key = os.environ["OPENAI_API_KEY"]

oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl="token")


def api_key_auth(api_key: str = fastapi.Depends(oauth2_scheme)):
    if api_key not in SIGNED_API_KEY:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Forbidden")


class ChatGPTSentence(pydantic.BaseModel):
    role: str
    content: str

class ChatGPTConversation(pydantic.BaseModel):
    sentence: list[ChatGPTSentence]
    temperature: float = 0.6

class ChatGPTOneSentenceOnly(pydantic.BaseModel):
    sentence: str
    temperature: float = 0.6

class ChatGPTConversationReply(pydantic.BaseModel):
    response: str
    total_tokens: int
    completion_tokens: int

app = fastapi.FastAPI()


@app.get("/gpt/multiround", dependencies=[fastapi.Depends(api_key_auth)])
def get_gpt_multiround(chat: ChatGPTConversation)->ChatGPTConversationReply:
    tmp0 = chat.model_dump()['sentence']
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=tmp0, temperature=chat.temperature)
    ret = {'response': response.choices[0].message.content,
            'total_tokens': response["usage"]["total_tokens"],
            'completion_tokens': response['usage']['completion_tokens']}
    return ret

@app.get("/gpt/oneround")
def get_gpt_oneround(message: ChatGPTOneSentenceOnly)->ChatGPTConversationReply:
    if message.sentence:
        tmp0 = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message.sentence},
        ]
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=tmp0, temperature=message.temperature)
        ret = {'response': response.choices[0].message.content,
                'total_tokens': response["usage"]["total_tokens"],
                'completion_tokens': response['usage']['completion_tokens']}
    else:
        ret = {'response': '', 'total_tokens':0, 'completion_tokens': 0}
    return ret

# uvicorn draft_server:app --port 9803 --host 0.0.0.0
