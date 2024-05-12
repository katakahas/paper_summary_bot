import os
from re import compile

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import gpt_read
import semantic_utils

app_token = os.getenv("SLACK_APP_TOKEN")
bot_token = os.getenv("SLACK_BOT_TOKEN")

app = App(token=bot_token)


# responce to "test" message in text channel
@app.message(compile("^test$"))
def test_function(body):
    main_event = body["event"]
    # text = main_event["text"]
    channel = main_event["channel"]

    app.client.chat_postMessage(text="test accepted", channel=channel)
    print("test command is accepted")


# retrieve url and return summary
@app.event("message")
def handle_message_events(body):
    main_event = body["event"]
    text_block = main_event["blocks"]
    text_elements = text_block[0]["elements"][0]["elements"]
    channel = main_event["channel"]

    # retrieve url
    url = ""
    for element in text_elements:
        if element["type"] == "link":
            url = element["url"]
            print("got url: " + url)

    # process arXiv url
    if url != "" and url.split("/")[2] == "arxiv.org":
        print("start translation")
        data_en = semantic_utils.paper_informations(
            url, item={"fields": "title,tldr,abstract,authors,venue,year,citationCount"}
        )
        # title_en = info_en[0]
        title_tldr_abs_en = data_en["title"], data_en["tldr"]["text"], data_en["abstract"]
        # title_ja, tldr_ja, abstract_ja = title_tldr_abs_en
        title_ja, tldr_ja, abstract_ja = gpt_read.translate_title_tldr_abs(*title_tldr_abs_en)
        message = "*タイトル*: " + title_ja + "\n"
        message += "*TL;DR*: " + tldr_ja + "\n"
        message += "*概要*: " + abstract_ja

        # get side information
        year = data_en["year"]
        venue = data_en["venue"]
        cites = data_en["citationCount"]
        authors = ""
        for item in data_en["authors"]:
            authors += item["name"] + ", "
        authors = authors[:-2]
        additional_info = "*Authors*: " + authors
        if venue is not None:
            additional_info += "\n*Venue*: " + venue
        if year is not None:
            additional_info += ", " + str(year)
        if cites is not None:
            additional_info += "\n*Cited by*: " + str(cites)

        # post message
        app.client.chat_postMessage(
            blocks=[
                {"type": "header", "text": {"type": "plain_text", "text": data_en["title"]}},
                {
                    "type": "context",
                    "elements": [
                        {"type": "mrkdwn", "text": "*Author*: " + authors},
                        {"type": "mrkdwn", "text": "*Venue*: " + venue + " " + str(year)},
                        {"type": "mrkdwn", "text": "*Cited by*: " + str(cites)},
                    ],
                },
                {"type": "section", "text": {"text": message, "type": "mrkdwn"}},
            ],
            text=message,
            channel=channel,
        )


# run app bot
if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()
