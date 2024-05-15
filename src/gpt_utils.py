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
    return f"以下の文章を日本語に翻訳した文のみを出力してください:\n{en}"


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
        run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)

        assert run.status == "completed", "Failed to complete the thread."

        vs_id = assistant.tool_resources.to_dict()["file_search"]["vector_store_ids"][0]
        response_delete_vs = client.beta.vector_stores.delete(vector_store_id=vs_id)
        response_delete_assistant = client.beta.assistants.delete(assistant.id)

        assert response_delete_vs.deleted, "Failed to delete vector store."
        assert response_delete_assistant.deleted, "Failed to delete assistant."

        return thread
    except BaseException as e:
        print(f"{e.__class__.__name__}: {e}")
        raise e


def create_assistant(client: OpenAI, save_path: str):
    vector_store = client.beta.vector_stores.create(name="PDFstore")
    with open(save_path, "rb") as f:
        _ = client.beta.vector_stores.file_batches.upload_and_poll(vector_store_id=vector_store.id, files=[f])
    print("PDF file uploaded.")

    os.remove(save_path)

    assistant = client.beta.assistants.create(
        instructions="You are a machine learning researcher. \
            You have to summarize the given paper on machine learning in the following format:\n\n\
            *Summary*:\n\
            *Pros*:\n\
            *Cons*:\n\
            *技術的な新規性*:\n\
            *実験評価*:\
            ",
        model="gpt-4o",
        name="KumaAssistant",
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
                "content": "与えられた機械学習に関する論文のPDFの要約をslackのmrkdwn記法で出力してください。slackのmrkdwn記法の一部は以下の通りです:\n\
                太字: *`対象のテキスト`*\n\
                斜体: _`対象のテキスト`_\n\
                箇条書き: ・`対象のテキスト`",
            }
        ]
    )
    return thread
