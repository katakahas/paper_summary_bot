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
        "model": "gpt-4o",
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


def call_gpt(client: OpenAI, save_path: str):
    try:
        assistant = create_assistant(client, save_path)
        thread = create_thread(client)
        _ = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)
        return thread
    except BaseException as e:
        print(f"{e.__class__.__name__}: {e}")
        raise e


def create_assistant(client: OpenAI, save_path: str):
    vector_store = client.beta.vector_stores.create(name="PDFstore")
    file_streams = [open(save_path, "rb")]
    _ = client.beta.vector_stores.file_batches.upload_and_poll(vector_store_id=vector_store.id, files=file_streams)
    assistant = client.beta.assistants.create(
        instructions="You are a machine learning researcher. Summarize the given paper on machine learning.",
        model="gpt-4o",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        temperature=0,
    )
    return assistant


def create_thread(client: OpenAI):
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "与えられた機械学習に関する論文のPDFを読み、この論文のSummary、ProsとCons、技術的な新規性、実験で何を評価したのかを以下のような形式で日本語で述べてください。\
                            ### Summary:\
                            ### Pros:\
                            ### Cons:\
                            ### 技術的な新規性:\
                            ### 実験評価:\
                            ",
            }
        ]
    )
    return thread
