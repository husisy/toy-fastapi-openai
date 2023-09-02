# toy-fastapi-openai

```bash
mamba create -n toy-fastapi-openai
mamba install -n toy-fastapi-openai fastapi pydantic openai uvicorn python-dotenv
```

server side

```bash
cp .env.example .env
# edit .env
uvicorn draft_server:app --port 9803
```

client side, see `draft_client.py`

```bash
cp .env.example .env
# edit .env
python draft_client.py
```

to generate apikey

```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```
