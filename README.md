# Slack Bot to Summarize Paper from URL
1. slackに投げられたメッセージからurlを抽出
2. urlをchatGPTに投げて、出力をbotが返信

# How to Run Bot
* 各環境変数(SLACK_APP_TOKEN,SLACK_BOT_TOKEN)にbotのapi tokenを設定しておく
* main.pyを走らせている間、研究室内のbotが動く(botは#b4_2023に導入済み)

# What to Do
* urlをchatGPTに投げて反応を得る
* みんなが興味がありそうな論文を定期的にレコメンドする

# Libraries
pip install -r requirements.txt