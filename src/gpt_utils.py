import os

from openai import AsyncOpenAI, OpenAI


def create_client() -> OpenAI:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_KUMA"), timeout=10000, max_retries=3)
    return client


def create_asyncClient() -> AsyncOpenAI:
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY_KUMA"), timeout=15, max_retries=3)
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
    }


def translation_prompt(en):
    return f"日本語に翻訳してください:\n{en}"


def fulltext_summary_prompt(url):
    return f"次の機械学習に関する論文のSummary、Pros.とCons.、技術的な新規性、実験で何を評価したのかを日本語で述べてください:\n{url}"


def summarize_pdf(pdf_url):
    # TODO: implement
    pass


async def call_gpt_async(client: AsyncOpenAI, prompt: str) -> tuple[str, int]:
    try:
        res = await client.chat.completions.create(**create_request(prompt))
        tokens = res.usage.total_tokens
        return res.choices[0].message.content, tokens
    except BaseException as e:
        print(f"{e.__class__.__name__}: {e}")
        raise e


def call_gpt(client: OpenAI, prompt: str) -> tuple[str, int]:
    try:
        res = client.chat.completions.create(**create_request(prompt))
        tokens = res.usage.total_tokens
        return res.choices[0].message.content, tokens
    except BaseException as e:
        print(f"{e.__class__.__name__}: {e}")
        raise e
