import os
from re import compile
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app_token = os.environ["SLACK_APP_TOKEN"]
bot_token = os.environ["SLACK_BOT_TOKEN"]

app = App(token=bot_token)

@app.message(compile("^私の名前は.+"))
def listener(body):
    main_event = body["event"]
    text = main_event["text"]
    channel = main_event["channel"]
    
    print(f"Text message: {text}")
    app.client.chat_postMessage(text="google pixelを使っています", channel=channel)

@app.event("message")
def handle_message_events(body, logger):
    print("invalid message")
    logger.info(body)
    
@app.event("message.im")
def direct_message(body):
    print(body)
    print("direct messaged")

if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()
