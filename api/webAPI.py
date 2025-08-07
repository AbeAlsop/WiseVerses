from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chat import Chatter
from dotenv import load_dotenv
import logging
import os
from pydantic import BaseModel

load_dotenv()
log_file_path = os.getenv('LOG_FILE_PATH')
if log_file_path:
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%y-%m-%d %H:%M:%S',
    )
logging.getLogger("httpx").setLevel(logging.WARNING)

app = FastAPI(root_path="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)

chat_bot = Chatter()

class ChatMessage(BaseModel):
    session: str
    message: str

@app.get("/")
def read_root():
    return {"Description": "WiseVerses API v0.1"}

@app.get("/response")
def read_response(q: str):
    response = chat_bot.respond_with_context(q, "global")
    logging.info(f"Received query: {q} | Responding: {response}")
    return {"Response": response}

@app.post("/response")
def post_response(prompt: ChatMessage):
    response = chat_bot.respond_with_context(prompt.message, prompt.session)
    quotes = " ".join([q['Quote'] for q in response['Quotes']])
    logging.info(f"Session: {prompt.session} | Received query: {prompt.message} | Quotes: {quotes} | Explanation: {response['Explanation']}")
    return response
