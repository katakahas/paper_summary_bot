import os

from openai import OpenAI


def get_client() -> OpenAI:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_KUMA"))
    return client


def create_request(prompt):
    return {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant and have a plenty of knowledge about informatics.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        # "timeout": 15,
    }


def translation_prompt(en):
    return f"日本語に翻訳してください:\n{en}"


def summarize_pdf(pdf_url):
    # TODO: implement
    pass


def call_gpt(prompt):
    client = get_client()
    res = client.chat.completions.create(**create_request(prompt))
    tokens = res.usage.total_tokens
    print(f"total tokens: {tokens}")
    return res.choices[0].message.content  # , tokens
