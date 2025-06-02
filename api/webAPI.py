from fastapi import FastAPI
from chat import Chatter
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(root_path="/api")
chat_bot = Chatter()

@app.get("/")
def read_root():
    return {"Description": "WiseVerses API v0.1"}

@app.get("/response")
def read_response(q: str):
    return {"Response": chat_bot.respond(q)}
