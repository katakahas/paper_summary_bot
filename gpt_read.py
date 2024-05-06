import openai
import os

OpenAI_api_key = os.environ["OPENAI_API_KEY"]

client = openai.OpenAI(api_key=OpenAI_api_key)

# GPTによる応答生成
prompt = "以下の条件の下でおいしい食べ物を教えてください。\n条件1:和食\n条件2:甘い"
response = client.chat.completions.create(
                    model = "gpt-3.5-turbo-16k-0613",
                    messages = [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0
                )

# 応答の表示
print(response)
text = response['choices'][0]['message']['content']
print(text)
