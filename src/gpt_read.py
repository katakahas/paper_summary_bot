from gpt_utils import call_gpt, translation_prompt


def summarize_paper_in_url(url):
    pass


def translate_title_tldr_abs(title, tldr, abs):
    def translate(en):
        prompt_en = translation_prompt(en)
        return call_gpt(prompt_en)

    return translate(title), translate(tldr), translate(abs)
