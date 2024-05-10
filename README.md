# Slack Bot to Summarize Paper from URL
1. slackに投げられたメッセージからurlを抽出
2. urlをchatGPTに投げて、出力をbotが返信

# How to Run Bot
* 各環境変数(SLACK_APP_TOKEN,SLACK_BOT_TOKEN)にbotのapi tokenを設定しておく
* main.pyを走らせている間、研究室内のbotが動く(botは#b4_2023に導入済み)

# What to Do
* urlをchatGPTに投げて反応を得る
  * semantic scholarから、引用数、査読済みなどの情報を取ってくる 
* みんなが興味がありそうな論文を定期的にレコメンドする

# Libraries
pip install -r requirements.txt

# Setting up virtual environment
1. `poetry` , `pyenv` を(頑張って)インストールする
2. このリポジトリを `git clone` する
4. `pyenv install 3.10.11` する
3. `git clone` してきたディレクトリ(以下、そこでのコマンド)で `poetry install` を叩く
5. `pre-commit install` を叩く
6. **(最重要)** ↑で作られた `paper_summary_bot/.git/hooks/pre-commit` (ファイル)を↓のように編集する

```shell
 #!/bin/sh
 . .\\.venv\\Scripts\\activate
 #!/usr/bin/env bash
 ...
```

ダメだったらご一報ください。