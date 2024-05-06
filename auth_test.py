import os
from slack_sdk.web import WebClient
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
response = client.auth_test()
print(response)