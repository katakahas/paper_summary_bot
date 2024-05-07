import os
import random
from re import compile
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app_token = os.environ["SLACK_APP_TOKEN"]
bot_token = os.environ["SLACK_BOT_TOKEN"]

app = App(token=bot_token)

@app.message(compile("test"))
def test_function(body):
    main_event = body["event"]
    text = main_event["text"]
    channel = main_event["channel"]
    
    app.client.chat_postMessage(text="test message", channel=channel)
    print("test command is accepted")

@app.event("message")
def handle_message_events(body):
    main_event = body["event"]
    text_block = main_event["blocks"]
    text_elements = text_block[0]["elements"][0]["elements"]
    
    for element in text_elements:
        if element["type"]=="link":
            url = element["url"]
            print("get url: "+url)

if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()
