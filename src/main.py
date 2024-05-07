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
def handle_message_events(body, logger):
    print("invalid message")
    logger.info(body)

if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()
