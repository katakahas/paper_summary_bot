import asyncio
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
        print("URL detected.")
        data_en = semantic_utils.paper_informations(
            url, item={"fields": "title,tldr,abstract,authors,venue,year,citationCount"}
        )
        # title_en = info_en[0]
        title_tldr_abs_en = data_en["title"], data_en["tldr"]["text"], data_en["abstract"]
        # title_ja, tldr_ja, abstract_ja = title_tldr_abs_en
        title_ja, tldr_ja, abstract_ja = asyncio.run(gpt_read.translate_tpl_en_async(*title_tldr_abs_en))
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

        # post message
        app.client.chat_postMessage(
            blocks=[
                {"type": "header", "text": {"type": "plain_text", "text": data_en["title"]}},
                {
                    "type": "context",
                    "elements": [
                        {"type": "mrkdwn", "text": ":student: *Author*: " + authors},
                        {"type": "mrkdwn", "text": ":pushpin: *Venue*: " + venue + " " + str(year)},
                        {"type": "mrkdwn", "text": ":black_nib: *Cited by*: " + str(cites)},
                    ],
                },
                {
                    "type": "rich_text",
                    "elements": [
                        {
                            "type": "rich_text_section",
                            "elements": [
                                {"type": "text", "text": "タイトル: ", "style": {"bold": True}},
                                {"type": "link", "url": url, "text": title_ja},
                                {"type": "text", "text": "\nTL;DR: ", "style": {"bold": True}},
                                {"type": "text", "text": tldr_ja},
                                {"type": "text", "text": "\n概要: ", "style": {"bold": True}},
                                {"type": "text", "text": abstract_ja},
                            ],
                        }
                    ],
                },
            ],
            text=message,
            channel=channel,
        )


# run app bot
if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()
