from slack_sdk.web import WebClient
client = WebClient()
response = client.api_test()
print(response)