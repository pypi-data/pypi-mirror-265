# Telebot Memory (telebot_mem)
Telebot with memory extension. It supports add a database backend to save chat histories.

## Quick start
Install from Pypi or from source
### [PyPi](https://pypi.org/project/telebot-mem/)
```bash
python3 -m pip install telebot-mem
```
Start a docker instance of mongo for quick experimentation
```bash
mkdir -p local/db
docker run -v ./local/db/:/data/db --rm -d -p 27017:27017 --name=mongo-test mongo:latest
```

```python
memdb = MongoMem("mongodb://localhost:27017/", "telegram")

@bot.message_handler(func=lambda message: True)
@memdb.memorize
def echo_message(message):
    ...
```
Refer to [echo bot example with mongodb](examples/echo_bot_mongo_example.py)

## Roadmap
### Beta (v0.x) API will subject to change
- [x] Test interface for mongodb support
