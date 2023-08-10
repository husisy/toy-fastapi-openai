# toy-fastapi-openai

```bash
mamba create -n toy-fastapi-openai
mamba install -n toy-fastapi-openai fastapi pydantic openai uvicorn python-dotenv
```

server side

```bash
cp .env.example .env
# edit .env
uvicorn draft00:app --port 9803
```

client side, see `draft01.py`

```bash
cp .env.example .env
# edit .env
python draft01.py
```
