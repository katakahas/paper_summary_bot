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
    channel = main_event["channel"]
    channel_type = main_event["channel_type"]

    app.client.chat_postMessage(text="test accepted", channel=channel)
    print("test command is accepted" + "channel_type: " + channel_type)


def post_paper(url, channel, title=True, tldr=True, abstract=True, summarize=True):
    data_en = semantic_utils.paper_informations(
        url, item={"fields": "title,tldr,abstract,authors,venue,year,citationCount"}
    )

    # construct text
    title_tldr_abs_en = data_en["title"], data_en["tldr"]["text"], data_en["abstract"]
    title_ja, tldr_ja, abstract_ja = asyncio.run(gpt_read.translate_tpl_en_async(*title_tldr_abs_en))
    message = "*タイトル*: " + title_ja + "\n"
    message += "*TL;DR*: " + tldr_ja + "\n"
    message += "*概要*: " + abstract_ja
    text_elements = []
    if title:
        text_elements.append({"type": "text", "text": "タイトル: ", "style": {"bold": True}})
        text_elements.append({"type": "link", "url": url, "text": title_ja})
    if tldr:
        text_elements.append({"type": "text", "text": "\nTL;DR: ", "style": {"bold": True}})
        text_elements.append({"type": "text", "text": tldr_ja})
    if abstract:
        text_elements.append({"type": "text", "text": "\n概要: ", "style": {"bold": True}})
        text_elements.append({"type": "text", "text": abstract_ja})

    # construct context
    year, venue, cites, authors = None, None, None, None
    try:
        year = data_en["year"]
    except KeyError as e:
        print(e)
    try:
        venue = data_en["venue"]
    except KeyError as e:
        print(e)
    try:
        cites = data_en["citationCount"]
    except KeyError as e:
        print(e)
    try:
        author_list = []
        for item in data_en["authors"]:
            author_list.append(item["name"])
        authors = ", ".join(author_list)
    except KeyError as e:
        print(e)
    context_elements = []
    if authors is not None:
        context_elements.append({"type": "mrkdwn", "text": ":student: *Author*: " + authors})
    if venue is not None and year is not None:
        context_elements.append({"type": "mrkdwn", "text": ":pushpin: *Venue*: " + venue + " " + str(year)})
    if cites is not None:
        context_elements.append({"type": "mrkdwn", "text": ":black_nib: *Cited by*: " + str(cites)})

    # construct message blocks
    header = {"type": "header", "text": {"type": "plain_text", "text": data_en["title"]}}
    context = {
        "type": "context",
        "elements": context_elements,
    }
    rich_text = {
        "type": "rich_text",
        "elements": [
            {
                "type": "rich_text_section",
                "elements": text_elements,
            }
        ],
    }
    message_blocks = [header, context, rich_text]

    # post message
    semantic = app.client.chat_postMessage(
        blocks=message_blocks,
        text=message,
        channel=channel,
    )

    if summarize:
        # get the full-text summary
        print("make summary")
        summary = gpt_read.summarize_paper_in_url(url)

        app.client.chat_postMessage(
            text=summary,
            channel=channel,
            thread_ts=semantic["message"]["ts"],
            blocks=[{"type": "section", "text": {"type": "mrkdwn", "text": summary}}],
        )

    return semantic


# retrieve url and return summary
@app.event("message")
def handle_message_events(body):
    try:
        main_event = body["event"]
        text_block = main_event["blocks"]
        text_elements = text_block[0]["elements"][0]["elements"]
        channel = main_event["channel"]
        # ignore bot message
        user_id = main_event["user"]
        user_info = app.client.users_info(user=user_id)
        if user_info["user"]["is_bot"]:
            return
    except KeyError as e:
        print(e)
        return

    # retrieve url
    url = ""
    for element in text_elements:
        if element["type"] == "link":
            url = element["url"]
            print("got url: " + url)

    # process arXiv url
    if url != "" and url.split("/")[2] == "arxiv.org":
        print("URL detected.")
        post_paper(url, channel)


# run app bot
if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()
