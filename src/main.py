import os
from re import compile
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from gpt_read import summarize_paper_in_url

app_token = os.environ["SLACK_APP_TOKEN"]
bot_token = os.environ["SLACK_BOT_TOKEN"]

app = App(token=bot_token)

# responce to "test" message in text channel
@app.message(compile("test"))
def test_function(body):
    main_event = body["event"]
    text = main_event["text"]
    channel = main_event["channel"]
    
    app.client.chat_postMessage(text="test message", channel=channel)
    print("test command is accepted")

# retrieve url and return summary
@app.event("message")
def handle_message_events(body):
    main_event = body["event"]
    text_block = main_event["blocks"]
    text_elements = text_block[0]["elements"][0]["elements"]
    channel = main_event["channel"]
    
    for element in text_elements:
        if element["type"]=="link":
            url = element["url"]
            print("get url: "+url)
            
    app.client.chat_postMessage(text=summarize_paper_in_url(url), channel=channel)

# run app bot
if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()
