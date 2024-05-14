import asyncio
import re

from arxiv_utils import load_pdf
from gpt_utils import (
    call_gpt,
    call_gpt_async,
    create_asyncClient,
    create_client,
    translation_prompt,
)


def summarize_paper_in_url(url: str) -> str:
    save_path = load_pdf(url)
    client = create_client()
    thread = call_gpt(client, save_path)
    thread_messages = client.beta.threads.messages.list(thread.id)
    response = thread_messages.data[0].content[0].text.value
    response = re.sub("【.*?source】。", "。", response)
    return response


def split_en(en: str) -> list[str]:
    def should_split(li_word: list[str]) -> list[bool]:
        """
        Return list of bool, where an index represents whether to sum up the word at that index.

        :param li_word: list of str
        :return: list of bool
        """
        while len(li_word) > 0 and li_word[-1] == "":
            li_word.pop(-1)

        li_bool = [False] * len(li_word)

        for i, word in enumerate(li_word):
            # if word is end of list, then True
            if i == len(li_word) - 1:
                li_bool[i] = True
            # if the next word starts with a capital letter...
            elif li_word[i + 1][0].isupper():
                # if word ends with [".", "!", "?"], then True
                if word.endswith(".") or word.endswith("!") or word.endswith("?"):
                    li_bool[i] = True
        return li_bool

    li_word = en.split()
    li_bool = should_split(li_word)
    li_sentence = []
    sentence = ""
    for word, flag in zip(li_word, li_bool):
        if flag:
            sentence += word
            li_sentence.append(sentence)
            sentence = ""
        else:
            sentence += word + " "
    return li_sentence


async def translate_tpl_en_async(*tpl_en: str) -> list[str]:
    async def translate_async(en: str) -> str:
        client = create_asyncClient()
        li_en = split_en(en)
        li_prompt = [translation_prompt(en) for en in li_en]
        tasks = [asyncio.create_task(call_gpt_async(client, prompt)) for prompt in li_prompt]
        res = await asyncio.gather(*tasks)
        li_ja, li_tokens = zip(*res)
        print(f"Total tokens: {sum(li_tokens)}")
        return "".join(li_ja)

    tasks = [asyncio.create_task(translate_async(en)) for en in tpl_en]
    res = await asyncio.gather(*tasks)
    return ["".join(r) for r in res]
