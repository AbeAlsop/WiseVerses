# Press Shift+F10 or the play button to execute
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging

from chat import Chatter

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

def dialogue():
    chat_bot = Chatter()
    context = "console"
    print("What's up?")
    while True:
        user_input = input()
        if user_input == "exit" or user_input == "quit":
            break
        response = chat_bot.respond_with_context(user_input, context)
        print(response)


if __name__ == '__main__':
    dialogue()


