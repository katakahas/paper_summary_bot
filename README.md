# Slack Bot to Summarize Paper from URL
1. slackに投げられたメッセージからurlを抽出
2. urlをchatGPTに投げて、出力をbotが返信

# How to Run Bot
各環境変数(SLACK_APP_TOKEN,SLACK_BOT_TOKEN)にbotのapi tokenを設定しておく
main.pyを走らせている間、研究室内のbotが動く(botは#b4_2023に導入済み)

# What to Do
* urlを含むメッセージに反応して、urlを抽出
* urlが論文のものであるか判定
* urlをchatGPTに投げて反応を得る
* chatGPTの反応をチャンネルへ返信

# Libraries
pip install -r requirements.txt