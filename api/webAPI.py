from fastapi import FastAPI
from chat import Chatter
from dotenv import load_dotenv
import logging
import os

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

chat_bot = Chatter()

@app.get("/")
def read_root():
    return {"Description": "WiseVerses API v0.1"}

@app.get("/response")
def read_response(q: str):
    response = chat_bot.respond(q)
    logging.info(f"Received query: {q} | Responding: {response}")
    return {"Response": response}
